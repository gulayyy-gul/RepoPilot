import gradio as gr
from core import RepoPilot

pilot = None


def analyze(url, key):
    global pilot
    if not url or not url.strip():
        return "Please enter a GitHub repository URL."
    try:
        pilot = RepoPilot(url.strip(), key.strip() if key else None)
        info = pilot.build_index()
        languages = ", ".join(info.get("languages", [])) or "Not detected"
        tests = len(info.get("tests", [])) if isinstance(info.get("tests"), list) else info.get("tests", "Not detected")
        docs = len(info.get("docs", [])) if isinstance(info.get("docs"), list) else info.get("docs", "Not detected")
        return (
            f"**Repository ready**  \n"
            f"`{info['name']}`  ·  Branch: `{info['branch']}`  ·  Files: **{info['files']}**  ·  "
            f"Chunks: **{info['chunks']}**  ·  Languages: **{languages}**  ·  "
            f"Tests: **{tests}**  ·  Docs: **{docs}**"
        )
    except Exception as e:
        pilot = None
        return f"**Analysis failed**  \n`{str(e)}`"


def ask(question):
    if pilot is None:
        return "### Connect a repository first\nAnalyze a GitHub repository before asking questions."
    if not question or not question.strip():
        return "Please enter a question."
    try:
        answer, sources = pilot.answer(question.strip())
        source_text = "\n".join(f"- `{s}`" for s in sources) if sources else "- No source files returned."
        return f"{answer}\n\n### Sources\n{source_text}"
    except Exception as e:
        return f"### Q&A error\n`{str(e)}`"


def load_prs():
    if pilot is None:
        return gr.update(choices=[], value=None), "Analyze a repository first."
    try:
        prs = pilot.list_pull_requests()
        choices = [f"#{p['number']} — {p['title']}" for p in prs]
        return gr.update(choices=choices, value=choices[0] if choices else None), (
            f"{len(prs)} open pull request(s) found." if prs else "No open pull requests found."
        )
    except Exception as e:
        return gr.update(choices=[], value=None), f"**PR loading failed:** `{str(e)}`"


def review_pr(selection):
    if pilot is None:
        return "Analyze a repository first."
    if not selection:
        return "Select a pull request first."
    try:
        number = int(selection.split(" — ", 1)[0].replace("#", "").strip())
        prs = pilot.list_pull_requests()
        pr = next((p for p in prs if int(p["number"]) == number), None)
        if pr is None:
            return "Pull request not found."
        return pilot.review_pr(pr)
    except Exception as e:
        return f"### PR review error\n`{str(e)}`"


def load_test_files():
    if pilot is None:
        return gr.update(choices=[], value=None), "Analyze a repository first."
    try:
        files = getattr(pilot, "code_files", []) or list(pilot.files_data.keys())
        choices = [f for f in files if isinstance(f, str) and f.endswith(('.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.go', '.rs', '.cpp', '.c'))]
        return gr.update(choices=choices, value=choices[0] if choices else None), (
            f"{len(choices)} code file(s) available." if choices else "No supported code files found."
        )
    except Exception as e:
        return gr.update(choices=[], value=None), f"**File loading failed:** `{str(e)}`"


def generate_tests(path):
    if pilot is None:
        return "Analyze a repository first."
    if not path:
        return "Select a code file first."
    try:
        code = pilot.generate_tests(path)
        return f"```python\n{code}\n```"
    except Exception as e:
        return f"### Test generation error\n`{str(e)}`"


def check_docs():
    if pilot is None:
        return "Analyze a repository first."
    try:
        return pilot.check_docs()
    except Exception as e:
        return f"### Documentation check error\n`{str(e)}`"


CSS = """
:root { --bg:#040308; --panel:#0D1015; --panel2:#08090D; --text:#F9F9FD; --muted:#9C9EB4; --border:#1C2028; --green:#20FE6B; --blue:#28B1DC; --purple:#4C5EAF; }
body, .gradio-container { background:var(--bg) !important; color:var(--text) !important; font-family:Inter, ui-sans-serif, system-ui, sans-serif !important; }
.gradio-container { max-width:1500px !important; padding:0 !important; }
#app-shell { min-height:100vh; }
.sidebar { background:var(--panel2); border-right:1px solid var(--border); min-height:100vh; padding:28px 18px !important; }
.brand { font-size:22px; font-weight:800; letter-spacing:-.5px; margin-bottom:34px; }
.brand span { color:var(--green); }
.nav-title { color:#686B7E; font-size:10px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; margin:18px 8px 8px; }
.nav-btn button { background:transparent !important; border:0 !important; color:#A8AABC !important; text-align:left !important; justify-content:flex-start !important; border-radius:9px !important; min-height:42px !important; }
.nav-btn button:hover { background:#12161D !important; color:#fff !important; }
.nav-btn button:focus { box-shadow:none !important; }
.repo-mini { margin-top:auto; background:#0D1015; border:1px solid var(--border); border-radius:12px; padding:14px; }
.repo-mini .label { color:#696C7E; font-size:10px; text-transform:uppercase; letter-spacing:1px; }
.repo-mini .value { color:#F9F9FD; font-size:12px; margin-top:6px; overflow-wrap:anywhere; }
.workspace { padding:34px 42px 50px !important; }
.eyebrow { color:var(--green); font-size:11px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; }
.hero h1 { font-size:38px; line-height:1.08; letter-spacing:-1.5px; margin:7px 0 10px; }
.hero p { color:var(--muted); font-size:15px; max-width:690px; line-height:1.65; }
.section-title { font-size:18px; font-weight:700; margin:30px 0 12px; }
.card { background:var(--panel); border:1px solid var(--border); border-radius:14px; padding:18px; }
.stat { min-height:95px; }
.stat-label { color:#777A8D; font-size:11px; text-transform:uppercase; letter-spacing:1px; }
.stat-value { color:#F9F9FD; font-size:24px; font-weight:700; margin-top:8px; }
.gradio-textbox, .gradio-dropdown, textarea, input { background:#0A0C10 !important; border-color:var(--border) !important; color:#F9F9FD !important; }
button.primary { background:var(--green) !important; color:#031008 !important; border:0 !important; font-weight:750 !important; }
button.primary:hover { filter:brightness(1.05); }
button { border-color:var(--border) !important; }
.output-box { background:#0A0C10 !important; border:1px solid var(--border) !important; border-radius:12px !important; }
.markdown { color:#E9EAF0; }
.markdown h3 { color:#F9F9FD; margin-top:10px; }
.markdown code { color:#B7FFCE; background:#11151B; border:1px solid #1B2520; border-radius:5px; padding:2px 5px; }
.markdown a { color:var(--blue); }
.status { margin-top:10px; }
.tip { color:#777A8D; font-size:12px; }
@media (max-width:900px) { .sidebar { min-height:auto; border-right:0; border-bottom:1px solid var(--border); } .workspace { padding:25px 18px !important; } .hero h1 { font-size:30px; } }
"""

with gr.Blocks(title="RepoPilot — AI teammate for GitHub", css=CSS, theme=gr.themes.Base()) as demo:
    with gr.Row(elem_id="app-shell", equal_height=False):
        with gr.Column(scale=1, min_width=220, elem_classes=["sidebar"]):
            gr.Markdown('<div class="brand">Repo<span>Pilot</span></div>')
            gr.Markdown('<div class="nav-title">Workspace</div>')
            overview_btn = gr.Button("Overview", elem_classes=["nav-btn"])
            qa_btn = gr.Button("Code Q&A", elem_classes=["nav-btn"])
            pr_btn = gr.Button("PR Review", elem_classes=["nav-btn"])
            tests_btn = gr.Button("Test Generator", elem_classes=["nav-btn"])
            docs_btn = gr.Button("Docs Check", elem_classes=["nav-btn"])
            gr.Markdown('<div style="flex:1; min-height:180px"></div>')
            gr.Markdown('<div class="repo-mini"><div class="label">Current repository</div><div class="value">Connect a repository to begin</div></div>')

        with gr.Column(scale=5, elem_classes=["workspace"]):
            with gr.Column(visible=True) as overview_view:
                gr.Markdown('<div class="hero"><div class="eyebrow">AI teammate for GitHub</div><h1>Your repository, understood.</h1><p>RepoPilot analyzes your GitHub codebase so you can ask questions, review pull requests, generate tests, and keep documentation consistent.</p></div>')
                with gr.Row():
                    with gr.Column(elem_classes=["card", "stat"]):
                        gr.Markdown('<div class="stat-label">Files</div><div class="stat-value">—</div>')
                    with gr.Column(elem_classes=["card", "stat"]):
                        gr.Markdown('<div class="stat-label">Chunks</div><div class="stat-value">—</div>')
                    with gr.Column(elem_classes=["card", "stat"]):
                        gr.Markdown('<div class="stat-label">Language</div><div class="stat-value">—</div>')
                    with gr.Column(elem_classes=["card", "stat"]):
                        gr.Markdown('<div class="stat-label">Status</div><div class="stat-value">Idle</div>')
                gr.Markdown('<div class="section-title">Connect repository</div>')
                with gr.Row():
                    repo_url = gr.Textbox(label="GitHub repository URL", placeholder="https://github.com/owner/repository", scale=3)
                    groq_key = gr.Textbox(label="Groq API key (optional if configured in Secrets)", type="password", scale=2)
                analyze_btn = gr.Button("Analyze Repository →", variant="primary", elem_id="analyze")
                status = gr.Markdown("Ready when you are.", elem_classes=["status", "output-box"])
                gr.Markdown("Your repository is read-only in this MVP. No code is modified or pushed automatically.", elem_classes=["tip"])

            with gr.Column(visible=False) as qa_view:
                gr.Markdown('<div class="eyebrow">Codebase intelligence</div><h2>Ask your repository</h2>')
                question = gr.Textbox(label="Question", placeholder="How does authentication work in this repository?", lines=3)
                ask_btn = gr.Button("Ask RepoPilot →", variant="primary")
                qa_output = gr.Markdown(elem_classes=["output-box"])

            with gr.Column(visible=False) as pr_view:
                gr.Markdown('<div class="eyebrow">Pull request intelligence</div><h2>Review a pull request</h2>')
                with gr.Row():
                    pr_select = gr.Dropdown(label="Open pull requests", choices=[])
                    load_pr_btn = gr.Button("Refresh PRs")
                pr_status = gr.Markdown("Analyze a repository first.", elem_classes=["tip"])
                review_btn = gr.Button("Review Pull Request →", variant="primary")
                pr_output = gr.Markdown(elem_classes=["output-box"])

            with gr.Column(visible=False) as tests_view:
                gr.Markdown('<div class="eyebrow">Automated testing</div><h2>Generate tests</h2>')
                with gr.Row():
                    test_file = gr.Dropdown(label="Code file", choices=[])
                    load_test_btn = gr.Button("Refresh files")
                test_status = gr.Markdown("Analyze a repository first.", elem_classes=["tip"])
                generate_btn = gr.Button("Generate Tests →", variant="primary")
                test_output = gr.Markdown(elem_classes=["output-box"])

            with gr.Column(visible=False) as docs_view:
                gr.Markdown('<div class="eyebrow">Documentation health</div><h2>Check documentation consistency</h2>')
                gr.Markdown("RepoPilot compares documentation with the indexed codebase and highlights areas that may need attention.")
                docs_btn_run = gr.Button("Run Docs Check →", variant="primary")
                docs_output = gr.Markdown(elem_classes=["output-box"])

    def show_view(name):
        return (
            gr.update(visible=name == "overview"),
            gr.update(visible=name == "qa"),
            gr.update(visible=name == "pr"),
            gr.update(visible=name == "tests"),
            gr.update(visible=name == "docs"),
        )

    for button, name in [(overview_btn, "overview"), (qa_btn, "qa"), (pr_btn, "pr"), (tests_btn, "tests"), (docs_btn, "docs")]:
        button.click(show_view, gr.State(name), [overview_view, qa_view, pr_view, tests_view, docs_view])

    analyze_btn.click(analyze, [repo_url, groq_key], status)
    ask_btn.click(ask, question, qa_output)
    load_pr_btn.click(load_prs, outputs=[pr_select, pr_status])
    review_btn.click(review_pr, pr_select, pr_output)
    load_test_btn.click(load_test_files, outputs=[test_file, test_status])
    generate_btn.click(generate_tests, test_file, test_output)
    docs_btn_run.click(check_docs, outputs=docs_output)

if __name__ == "__main__":
    demo.launch()
