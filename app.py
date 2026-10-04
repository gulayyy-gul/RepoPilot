import streamlit as st
from core import RepoPilot

st.set_page_config(page_title="RepoPilot", page_icon="🚀", layout="wide")
st.title("🚀 RepoPilot")
st.caption("AI teammate for understanding, reviewing, testing, and documenting GitHub repositories.")

with st.sidebar:
    st.header("Connect Repository")
    repo_url = st.text_input("Public GitHub repository URL", placeholder="https://github.com/owner/repository")
    st.caption("Hackathon MVP: use a public repository. No GitHub token is needed.")

    st.header("AI Key")
    try:
        secret_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        secret_key = ""
    if secret_key:
        st.success("Groq key detected.")
    else:
        st.warning("Add GROQ_API_KEY in Streamlit Secrets.")
    manual_key = st.text_input("Temporary Groq key (optional)", type="password")
    groq_key = manual_key or secret_key

    if st.button("Analyze Repository", type="primary", use_container_width=True):
        if not repo_url.strip():
            st.error("Paste a GitHub repository URL first.")
        else:
            try:
                with st.spinner("Fetching and indexing repository..."):
                    pilot = RepoPilot(repo_url.strip(), groq_key)
                    info = pilot.build_index()
                st.session_state.pilot = pilot
                st.session_state.info = info
                st.success("Repository is ready!")
            except Exception as e:
                st.error(f"Could not analyze repository: {e}")

pilot = st.session_state.get("pilot")
info = st.session_state.get("info")

if not pilot:
    st.info("👈 Paste a public GitHub repository URL and click **Analyze Repository**.")
    st.markdown("""
    ### What RepoPilot can do
    - 🔎 Codebase Q&A with source references
    - 🔍 Pull Request review
    - 🧪 Test generation
    - 📚 Documentation consistency checking
    """)
    st.warning("AI output is advisory. RepoPilot never modifies your repository.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Files indexed", info["files"])
c2.metric("Chunks", info["chunks"])
c3.metric("Languages", len(info["languages"]))
c4.metric("Status", "Ready")

st.subheader("Repository Overview")
st.write(f"**Repository:** {info['name']}")
st.write(f"**Languages:** {', '.join(info['languages']) or 'Not detected'}")
st.write(f"**Key directories:** {', '.join(info['directories']) or 'Root only'}")
st.write(f"**Tests:** {', '.join(info['tests']) or 'Not detected'}")
st.write(f"**Documentation:** {', '.join(info['docs']) or 'Not detected'}")

tabs = st.tabs(["💬 Codebase Q&A", "🔍 PR Review", "🧪 Test Generator", "📚 Docs Check"])

with tabs[0]:
    st.subheader("Ask your repository")
    q = st.text_input("Question", placeholder="Where is authentication implemented?")
    if st.button("Ask RepoPilot", key="ask"):
        if not q.strip():
            st.warning("Enter a question.")
        else:
            with st.spinner("Searching repository..."):
                answer, sources = pilot.answer(q)
            st.markdown("### Answer")
            st.write(answer)
            st.markdown("### Sources")
            for source in sources:
                st.code(source)
            st.caption("⚠️ AI-generated and advisory.")

with tabs[1]:
    st.subheader("Pull Request Review")
    prs = pilot.list_pull_requests()
    if not prs:
        st.info("No public open Pull Requests were found.")
    else:
        selected = st.selectbox("Select PR", range(len(prs)), format_func=lambda i: f"#{prs[i]['number']} — {prs[i]['title']}")
        if st.button("Review PR", key="review"):
            with st.spinner("Reviewing PR..."):
                st.markdown(pilot.review_pr(prs[selected]))
            st.caption("⚠️ Findings are advisory, not guaranteed.")

with tabs[2]:
    st.subheader("Test Generator")
    if pilot.code_files:
        selected_path = st.selectbox("Select a code file", pilot.code_files)
        if st.button("Generate Tests", key="tests"):
            with st.spinner("Generating tests..."):
                result = pilot.generate_tests(selected_path)
            st.code(result)
            st.caption("Review generated tests before using them.")
    else:
        st.info("No supported code files were indexed.")

with tabs[3]:
    st.subheader("Documentation Consistency Check")
    if st.button("Check Documentation", key="docs"):
        with st.spinner("Checking documentation..."):
            st.markdown(pilot.check_docs())
        st.caption("⚠️ Documentation findings are advisory.")

st.divider()
st.caption("RepoPilot MVP • Read-only • RAG-based repository assistant")
