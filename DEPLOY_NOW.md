# RepoPilot — Deploy Tonight

## 1. GitHub

Upload:
- app.py
- core.py
- gradio_ui.py
- requirements.txt
- README.md
- DEPLOY_NOW.md
- .gitignore
- .streamlit/config.toml
- .streamlit/secrets.toml.example

Do NOT upload a real `.env` or `secrets.toml`.

## 2. Streamlit

Create a new Streamlit app.

Select:
- Repository: your RepoPilot repository
- Branch: `main`
- Main file: `app.py`

Deploy.

## 3. Add Groq key

Open the deployed app's Settings → Secrets and paste:

```toml
GROQ_API_KEY = "YOUR_GROQ_KEY"
```

Save/reboot.

## 4. Test

Use a small public GitHub repository.

Try:
- "Explain the architecture."
- "Where is authentication implemented?"
- Select an open PR and review it.
- Select a code file and generate tests.
- Run the documentation check.

## 5. If time is very short

Demo in this order:
1. Analyze repository
2. Codebase Q&A
3. PR Review
4. Test Generator
5. Docs Check
