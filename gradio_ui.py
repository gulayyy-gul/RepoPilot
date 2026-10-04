import gradio as gr
from core import RepoPilot

pilot = None

def analyze(url, key):
    global pilot
    pilot = RepoPilot(url, key)
    info = pilot.build_index()
    return f"Ready: {info['name']} | Files: {info['files']} | Chunks: {info['chunks']} | Languages: {', '.join(info['languages']) or 'Not detected'}"

def ask(question):
    if pilot is None:
        return "Analyze a repository first."
    answer, sources = pilot.answer(question)
    return answer + "\n\nSources:\n" + "\n".join(sources)

with gr.Blocks(title="RepoPilot") as demo:
    gr.Markdown("# 🚀 RepoPilot\nAI teammate for a GitHub repository.")
    with gr.Row():
        url = gr.Textbox(label="Public GitHub URL")
        key = gr.Textbox(label="Groq API key", type="password")
    analyze_button = gr.Button("Analyze Repository", variant="primary")
    status = gr.Textbox(label="Status")
    analyze_button.click(analyze, [url, key], status)
    gr.Markdown("## Codebase Q&A")
    question = gr.Textbox(label="Question")
    ask_button = gr.Button("Ask")
    output = gr.Markdown()
    ask_button.click(ask, question, output)

if __name__ == "__main__":
    demo.launch()
