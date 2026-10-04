# 🚀 RepoPilot — Hackathon MVP

RepoPilot is a read-only AI teammate for GitHub repositories.

## Features
- Public GitHub repository analysis
- Lightweight RAG retrieval
- Codebase Q&A with source files
- Pull Request review
- Test generation
- Documentation consistency check
- Streamlit deployment
- Optional Gradio UI

## Deploy on Streamlit

1. Upload the project files to GitHub.
2. Do **not** upload a real `.env` or `.streamlit/secrets.toml`.
3. Create a Streamlit app using `app.py`.
4. Open the app's **Settings → Secrets**.
5. Add:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

6. Save/reboot.
7. Paste a **public GitHub repository URL** into RepoPilot.
8. Click **Analyze Repository**.

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Optional Gradio UI:

```bash
python gradio_ui.py
```

## Important MVP simplification

This version uses TF-IDF retrieval instead of adding a separate embedding API/vector database. It still follows the RAG flow: repository files are chunked, relevant chunks are retrieved, and only those chunks are sent to the LLM.

This avoids extra services and extra keys so the MVP can be deployed quickly.

## GitHub token

This emergency MVP is designed for **public repositories**, so it does not require a GitHub token. Private-repository OAuth can be added later.

## AI model

The app uses `openai/gpt-oss-120b` through Groq.
