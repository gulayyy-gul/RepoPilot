import base64
import os
import re
from urllib.parse import urlparse

import requests
from groq import Groq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SUPPORTED = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".go", ".rs", ".md", ".json", ".yaml", ".yml", ".toml", ".html", ".css"}
IGNORE_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", ".venv", "venv", ".next", "coverage"}
MAX_FILE_BYTES = 180_000
MAX_CHUNKS = 800


def parse_repo_url(url):
    p = urlparse(url)
    if p.netloc.lower() not in {"github.com", "www.github.com"}:
        raise ValueError("Please use a github.com repository URL.")
    parts = [x for x in p.path.strip("/").split("/") if x]
    if len(parts) < 2:
        raise ValueError("Use: https://github.com/owner/repository")
    return parts[0], parts[1].removesuffix(".git")


def ext(path):
    path = path.lower()
    for e in SUPPORTED:
        if path.endswith(e):
            return e
    return ""


def chunk_text(text, size=1200, overlap=150):
    text = text.replace("\r\n", "\n")
    if len(text) <= size:
        return [text]
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + size)
        if text[start:end].strip():
            chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


class RepoPilot:
    def __init__(self, repo_url, groq_api_key=None):
        self.repo_url = repo_url.rstrip("/")
        self.owner, self.repo = parse_repo_url(self.repo_url)
        self.groq_key = groq_api_key or os.getenv("GROQ_API_KEY", "")
        self.model = "openai/gpt-oss-120b"
        self.files_data, self.chunks = {}, []
        self.vectorizer, self.matrix = None, None
        self.code_files = []
        self.repo_info = {}

    def github_get(self, path, params=None):
        r = requests.get(f"https://api.github.com{path}", headers={"Accept": "application/vnd.github+json"}, params=params, timeout=25)
        if not r.ok:
            raise RuntimeError(f"GitHub API error {r.status_code}: {r.text[:250]}")
        return r.json()

    def fetch_tree(self):
        repo = self.github_get(f"/repos/{self.owner}/{self.repo}")
        branch = repo.get("default_branch", "main")
        tree = self.github_get(f"/repos/{self.owner}/{self.repo}/git/trees/{branch}", params={"recursive": "1"})
        return repo, branch, tree.get("tree", [])

    def build_index(self):
        _, branch, tree = self.fetch_tree()
        self.files_data, self.chunks, self.code_files = {}, [], []

        for item in tree:
            path = item.get("path", "")
            if item.get("type") != "blob" or not ext(path):
                continue
            if any(part in IGNORE_DIRS for part in path.split("/")):
                continue
            if item.get("size", 0) > MAX_FILE_BYTES:
                continue
            try:
                data = self.github_get(f"/repos/{self.owner}/{self.repo}/contents/{path}", params={"ref": branch})
                raw = data.get("content", "")
                text_value = base64.b64decode(raw).decode("utf-8", errors="ignore") if data.get("encoding") == "base64" else raw
            except Exception:
                continue

            self.files_data[path] = text_value
            if ext(path) not in {".md", ".json", ".yaml", ".yml", ".toml"}:
                self.code_files.append(path)
            for i, piece in enumerate(chunk_text(text_value)):
                self.chunks.append({"path": path, "chunk": i + 1, "text": piece})
                if len(self.chunks) >= MAX_CHUNKS:
                    break
            if len(self.chunks) >= MAX_CHUNKS:
                break

        if not self.chunks:
            raise RuntimeError("No supported text files were found.")

        self.vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2), max_features=30000)
        self.matrix = self.vectorizer.fit_transform([c["text"] for c in self.chunks])

        mapping = {".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".jsx": "React/JSX", ".tsx": "React/TSX", ".java": "Java", ".cpp": "C++", ".c": "C", ".go": "Go", ".rs": "Rust"}
        languages = []
        for p in self.files_data:
            name = mapping.get(ext(p))
            if name and name not in languages:
                languages.append(name)
        directories = sorted({p.split("/")[0] for p in self.files_data if "/" in p})[:12]
        tests = [p for p in self.files_data if re.search(r"(^|/)(tests?|__tests__)(/|$)|test_", p, re.I)][:12]
        docs = [p for p in self.files_data if p.lower().endswith((".md", ".rst")) or "readme" in p.lower()][:12]

        self.repo_info = {"name": f"{self.owner}/{self.repo}", "branch": branch, "files": len(self.files_data), "chunks": len(self.chunks), "languages": languages, "directories": directories, "tests": tests, "docs": docs}
        return self.repo_info

    def retrieve(self, query, k=6):
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        results = []
        for i in scores.argsort()[::-1][:k]:
            if scores[i] <= 0:
                continue
            result = dict(self.chunks[i])
            result["score"] = float(scores[i])
            results.append(result)
        return results

    def llm(self, system, user):
        if not self.groq_key:
            raise RuntimeError("Add GROQ_API_KEY in Streamlit Secrets.")
        client = Groq(api_key=self.groq_key)
        response = client.chat.completions.create(model=self.model, messages=[{"role": "system", "content": system}, {"role": "user", "content": user}], temperature=0.2, max_completion_tokens=1200)
        return response.choices[0].message.content

    def answer(self, question):
        hits = self.retrieve(question, 7)
        if not hits:
            return "I don't have enough evidence in the indexed repository to answer that.", []
        context = "\n\n".join(f"FILE: {h['path']}\n{h['text']}" for h in hits)
        answer = self.llm("""You are RepoPilot, a repository assistant. Answer only from the supplied repository context. Do not invent files, functions, dependencies, or behavior. If evidence is insufficient, say so. Mention relevant file paths. Keep the answer concise and practical.""", f"Question:\n{question}\n\nRepository context:\n{context}")
        return answer, list(dict.fromkeys(h["path"] for h in hits))[:5]

    def list_pull_requests(self):
        try:
            data = self.github_get(f"/repos/{self.owner}/{self.repo}/pulls", params={"state": "open", "per_page": 20})
            return [{"number": x["number"], "title": x["title"], "body": x.get("body") or ""} for x in data]
        except Exception:
            return []

    def review_pr(self, pr):
        files = self.github_get(f"/repos/{self.owner}/{self.repo}/pulls/{pr['number']}/files", params={"per_page": 50})
        diff = "\n\n".join(f"FILE: {f['filename']}\nPATCH:\n{f.get('patch','')[:6000]}" for f in files)
        related = []
        for f in files[:8]:
            related.extend(self.retrieve(f["filename"], 2))
        context = "\n\n".join(f"FILE: {h['path']}\n{h['text']}" for h in related[:12])
        return self.llm("""You are a careful senior code reviewer. Review only the supplied PR diff and repository context. Return Markdown findings. Each finding must contain Severity (High/Medium/Low), Category, File, Problem, Recommendation. Do not invent evidence. If no meaningful issue is found, say so.""", f"PR #{pr['number']}: {pr['title']}\nDescription:\n{pr['body'][:4000]}\n\nDIFF:\n{diff[:24000]}\n\nRELATED REPOSITORY CONTEXT:\n{context[:18000]}")

    def generate_tests(self, path):
        source = self.files_data.get(path, "")
        related = self.retrieve(path, 5)
        context = "\n\n".join(f"FILE: {h['path']}\n{h['text']}" for h in related)
        return self.llm("""Generate tests for the target repository. Infer the likely test framework from the context. Return only test code, without markdown fences. Do not invent APIs not visible in the context. Tests are suggestions and may need adjustment.""", f"Target file: {path}\n\nSOURCE:\n{source[:10000]}\n\nRELATED CONTEXT:\n{context[:12000]}")

    def check_docs(self):
        docs = "\n\n".join(f"FILE: {p}\n{self.files_data[p]}" for p in self.repo_info.get("docs", []))
        code = "\n\n".join(f"FILE: {p}\n{self.files_data[p][:5000]}" for p in self.code_files[:12])
        return self.llm("""Check documentation against repository code. Report only plausible, evidence-based inconsistencies. For each issue include Documentation file, Code evidence, Issue, and Suggested update. If evidence is insufficient, say so.""", f"DOCUMENTATION:\n{docs[:16000]}\n\nCODE:\n{code[:22000]}")
