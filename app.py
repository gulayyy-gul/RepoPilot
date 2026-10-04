import streamlit as st
from core import RepoPilot


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RepoPilot",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "page": "Overview",
    "pilot": None,
    "repo_url": "",
    "groq_key": "",
    "analysis_error": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------
       GLOBAL
    ------------------------- */

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #FAFAF8;
        color: #171717;
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 42px;
        padding-bottom: 80px;
    }

    /* Remove default top spacing */
    header {
        background: transparent !important;
    }

    /* -------------------------
       SIDEBAR
    ------------------------- */

    section[data-testid="stSidebar"] {
        background: #F4F4F1;
        border-right: 1px solid #E5E5E0;
    }

    section[data-testid="stSidebar"] > div {
        padding: 28px 22px;
    }

    .brand {
        font-family: 'Manrope', sans-serif;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.7px;
        color: #151515;
        margin-bottom: 38px;
    }

    .brand-mark {
        color: #16A34A;
        margin-right: 7px;
    }

    .side-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #969690;
        margin: 24px 0 9px 0;
    }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent;
        border: none;
        border-radius: 8px;
        color: #686863;
        text-align: left;
        justify-content: flex-start;
        padding: 9px 10px;
        font-size: 14px;
        font-weight: 500;
        transition: 0.15s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #EAEAE5;
        color: #171717;
    }

    /* -------------------------
       INPUTS
    ------------------------- */

    .stTextInput > div > div > input {
        background: #FFFFFF;
        border: 1px solid #DCDCD6;
        border-radius: 7px;
        color: #171717;
        padding: 13px 14px;
        font-size: 14px;
    }

    .stTextInput > div > div > input:focus {
        border-color: #AFAFA8;
        box-shadow: 0 0 0 1px #AFAFA8;
    }

    .stTextInput label {
        font-size: 12px;
        color: #777771;
    }

    /* -------------------------
       PRIMARY BUTTON
    ------------------------- */

    .stButton > button[kind="primary"] {
        background: #171717;
        color: #FFFFFF;
        border: 1px solid #171717;
        border-radius: 7px;
        padding: 11px 18px;
        font-size: 13px;
        font-weight: 600;
        transition: all 0.18s ease;
    }

    .stButton > button[kind="primary"]:hover {
        background: #16A34A;
        border-color: #16A34A;
        color: white;
    }

    /* -------------------------
       DIVIDERS
    ------------------------- */

    hr {
        border: none;
        border-top: 1px solid #E4E4DE;
        margin: 34px 0;
    }

    /* -------------------------
       TYPOGRAPHY
    ------------------------- */

    .eyebrow {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        color: #16A34A;
        margin-bottom: 18px;
    }

    .hero-title {
        font-family: 'Manrope', sans-serif;
        font-size: clamp(48px, 6vw, 82px);
        line-height: 0.98;
        letter-spacing: -4px;
        font-weight: 800;
        color: #171717;
        max-width: 850px;
        margin: 0;
    }

    .hero-title .accent {
        color: #16A34A;
    }

    .hero-subtitle {
        font-size: 17px;
        line-height: 1.65;
        color: #73736D;
        max-width: 560px;
        margin-top: 25px;
    }

    .section-number {
        font-size: 11px;
        font-weight: 700;
        color: #A0A09A;
        letter-spacing: 1px;
    }

    .section-title {
        font-family: 'Manrope', sans-serif;
        font-size: 27px;
        font-weight: 700;
        letter-spacing: -1px;
        color: #171717;
        margin: 0;
    }

    .small-muted {
        color: #85857E;
        font-size: 13px;
    }

    /* -------------------------
       REPOSITORY INFO
    ------------------------- */

    .repo-name {
        font-family: 'Manrope', sans-serif;
        font-size: 25px;
        font-weight: 700;
        letter-spacing: -0.8px;
        color: #171717;
    }

    .repo-meta {
        font-size: 13px;
        color: #777771;
        margin-top: 5px;
    }

    .repo-meta span {
        margin-right: 14px;
    }

    .status-ready {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        font-size: 12px;
        font-weight: 600;
        color: #16803A;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        background: #16A34A;
        border-radius: 50%;
        display: inline-block;
    }

    /* -------------------------
       WORKSPACE ROWS
    ------------------------- */

    .workspace-row {
        border-top: 1px solid #E1E1DB;
        padding: 22px 4px;
    }

    .workspace-row:last-child {
        border-bottom: 1px solid #E1E1DB;
    }

    .workspace-number {
        font-size: 11px;
        color: #A0A09A;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .workspace-name {
        font-family: 'Manrope', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: #171717;
        letter-spacing: -0.5px;
    }

    .workspace-description {
        font-size: 13px;
        color: #85857E;
        margin-top: 4px;
    }

    /* -------------------------
       RESULT AREA
    ------------------------- */

    .result-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        color: #999991;
        margin-bottom: 12px;
    }

    .result-content {
        font-size: 15px;
        line-height: 1.7;
        color: #292925;
    }

    .source-item {
        font-family: monospace;
        font-size: 12px;
        color: #5F5F59;
        padding: 5px 0;
    }

    /* -------------------------
       TABLE / SELECTBOX
    ------------------------- */

    .stSelectbox > div > div {
        background: #FFFFFF;
        border-color: #DCDCD6;
        border-radius: 7px;
    }

    /* -------------------------
       CODE
    ------------------------- */

    pre {
        border: 1px solid #E0E0DA !important;
        border-radius: 8px !important;
        background: #FFFFFF !important;
    }

    /* -------------------------
       MOBILE
    ------------------------- */

    @media (max-width: 800px) {

        .hero-title {
            font-size: 48px;
            letter-spacing: -2.5px;
        }

        .main .block-container {
            padding-left: 22px;
            padding-right: 22px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="brand"><span class="brand-mark">◈</span>RepoPilot</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-label">Workspace</div>', unsafe_allow_html=True)

    if st.button("Overview", use_container_width=True):
        st.session_state.page = "Overview"

    if st.button("Codebase Q&A", use_container_width=True):
        st.session_state.page = "Code Q&A"

    if st.button("PR Review", use_container_width=True):
        st.session_state.page = "PR Review"

    if st.button("Test Generator", use_container_width=True):
        st.session_state.page = "Test Generator"

    if st.button("Docs Check", use_container_width=True):
        st.session_state.page = "Docs Check"

    st.markdown('<div class="side-label">Repository</div>', unsafe_allow_html=True)

    repo_url = st.text_input(
        "GitHub repository",
        value=st.session_state.repo_url,
        placeholder="https://github.com/owner/repo",
        label_visibility="collapsed",
    )

    groq_key = st.text_input(
        "Groq API key",
        value=st.session_state.groq_key,
        type="password",
        placeholder="Groq API key",
        label_visibility="collapsed",
    )

    st.session_state.repo_url = repo_url
    st.session_state.groq_key = groq_key

    if st.button(
        "Analyze repository →",
        type="primary",
        use_container_width=True,
    ):
        if not repo_url.strip():
            st.session_state.analysis_error = "Enter a GitHub repository URL."
        else:
            try:
                with st.spinner("Analyzing repository..."):
                    pilot = RepoPilot(repo_url.strip(), groq_key.strip())
                    pilot.build_index()

                    st.session_state.pilot = pilot
                    st.session_state.analysis_error = ""

                st.session_state.page = "Overview"
                st.rerun()

            except Exception as e:
                st.session_state.analysis_error = str(e)

    if st.session_state.analysis_error:
        st.error(st.session_state.analysis_error)

    if st.session_state.pilot:
        st.markdown(
            """
            <div style="margin-top:30px;">
                <div class="side-label">Connection</div>
                <div class="status-ready">
                    <span class="status-dot"></span>
                    Repository ready
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# HELPERS
# ============================================================

def workspace_row(number, title, description):
    col1, col2, col3 = st.columns([0.08, 0.57, 0.35])

    with col1:
        st.markdown(
            f'<div class="workspace-number">{number}</div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="workspace-name">{title}</div>
            <div class="workspace-description">{description}</div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        if st.button(
            "Open →",
            key=f"open_{number}_{title}",
            use_container_width=True,
        ):
            st.session_state.page = title
            st.rerun()


def section_heading(number, title):
    st.markdown(
        f"""
        <div style="display:flex; gap:20px; align-items:baseline;">
            <div class="section-number">{number}</div>
            <div class="section-title">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# OVERVIEW
# ============================================================

if st.session_state.page == "Overview":

    st.markdown(
        '<div class="eyebrow">AI teammate for GitHub</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-title">
            Understand your codebase.<br>
            <span class="accent">Ship with confidence.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            RepoPilot analyzes your repository, answers questions,
            reviews pull requests, generates tests, and checks your
            documentation — all from one workspace.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Repository input on main page
    c1, c2 = st.columns([0.78, 0.22])

    with c1:
        main_repo_url = st.text_input(
            "Repository URL",
            value=st.session_state.repo_url,
            placeholder="https://github.com/owner/repository",
            label_visibility="collapsed",
            key="main_repo_input",
        )

    with c2:
        if st.button(
            "Analyze →",
            type="primary",
            use_container_width=True,
            key="main_analyze",
        ):
            if not main_repo_url.strip():
                st.error("Enter a GitHub repository URL.")
            else:
                try:
                    with st.spinner("Analyzing repository..."):
                        pilot = RepoPilot(
                            main_repo_url.strip(),
                            st.session_state.groq_key.strip(),
                        )

                        pilot.build_index()

                        st.session_state.pilot = pilot
                        st.session_state.repo_url = main_repo_url.strip()
                        st.session_state.analysis_error = ""

                    st.rerun()

                except Exception as e:
                    st.error(str(e))

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # Repository snapshot
    # --------------------------------------------------------

    section_heading("01", "Repository")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.pilot:

        info = st.session_state.pilot.repo_info

        st.markdown(
            f"""
            <div class="repo-name">{info['name']}</div>
            <div class="repo-meta">
                <span>{', '.join(info['languages']) or 'Language not detected'}</span>
                <span>·</span>
                <span>{info['branch']}</span>
                <span>·</span>
                <span>{info['files']} files</span>
                <span>·</span>
                <span>{info['chunks']} chunks</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="status-ready">
                <span class="status-dot"></span>
                Repository indexed and ready
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <div class="small-muted">
                Connect a GitHub repository to begin.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # Workspace
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    section_heading("02", "Workspace")

    st.markdown("<br>", unsafe_allow_html=True)

    workspace_row(
        "01",
        "Code Q&A",
        "Ask questions and understand your codebase.",
    )

    workspace_row(
        "02",
        "PR Review",
        "Find potential issues before changes reach production.",
    )

    workspace_row(
        "03",
        "Test Generator",
        "Generate tests from existing repository code.",
    )

    workspace_row(
        "04",
        "Docs Check",
        "Find clear inconsistencies between code and documentation.",
    )

    # --------------------------------------------------------
    # Repository insights
    # --------------------------------------------------------

    if st.session_state.pilot:

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        section_heading("03", "Repository insights")

        st.markdown("<br>", unsafe_allow_html=True)

        info = st.session_state.pilot.repo_info

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown('<div class="result-label">Languages</div>', unsafe_allow_html=True)
            st.markdown(
                ", ".join(info["languages"]) or "Not detected",
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown('<div class="result-label">Directories</div>', unsafe_allow_html=True)
            st.markdown(
                ", ".join(info["directories"]) or "None detected",
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown('<div class="result-label">Tests</div>', unsafe_allow_html=True)

            if info["tests"]:
                st.markdown(
                    f"{len(info['tests'])} test-related paths",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("No test paths detected")

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div class="result-label">Documentation</div>', unsafe_allow_html=True)

            if info["docs"]:
                for doc in info["docs"][:8]:
                    st.markdown(
                        f'<div class="source-item">{doc}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown("No documentation files detected.")

        with c2:
            st.markdown('<div class="result-label">Repository branch</div>', unsafe_allow_html=True)
            st.markdown(info["branch"])


# ============================================================
# CODE Q&A
# ============================================================

elif st.session_state.page == "Code Q&A":

    section_heading("01", "Codebase Q&A")

    st.markdown(
        """
        <div class="hero-subtitle">
            Ask RepoPilot anything about the indexed repository.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.pilot:
        st.info("Analyze a repository first.")
    else:

        question = st.text_area(
            "Question",
            placeholder="How is authentication handled in this repository?",
            height=110,
            label_visibility="collapsed",
        )

        if st.button("Ask RepoPilot →", type="primary"):

            if not question.strip():
                st.warning("Enter a question.")
            else:

                try:
                    with st.spinner("Searching the codebase..."):

                        answer, sources = st.session_state.pilot.answer(
                            question.strip()
                        )

                    st.markdown("<hr>", unsafe_allow_html=True)

                    st.markdown(
                        '<div class="result-label">Answer</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f'<div class="result-content">{answer}</div>',
                        unsafe_allow_html=True,
                    )

                    if sources:

                        st.markdown("<br>", unsafe_allow_html=True)

                        st.markdown(
                            '<div class="result-label">Sources</div>',
                            unsafe_allow_html=True,
                        )

                        for source in sources:
                            st.markdown(
                                f'<div class="source-item">{source}</div>',
                                unsafe_allow_html=True,
                            )

                except Exception as e:
                    st.error(str(e))


# ============================================================
# PR REVIEW
# ============================================================

elif st.session_state.page == "PR Review":

    section_heading("02", "Pull Request Review")

    st.markdown(
        """
        <div class="hero-subtitle">
            Review open pull requests using the repository context.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.pilot:

        st.info("Analyze a repository first.")

    else:

        try:

            prs = st.session_state.pilot.list_pull_requests()

            if not prs:

                st.info("No open pull requests found.")

            else:

                pr_options = {
                    f"#{pr['number']} — {pr['title']}": pr
                    for pr in prs
                }

                selected_label = st.selectbox(
                    "Pull request",
                    list(pr_options.keys()),
                )

                selected_pr = pr_options[selected_label]

                if st.button(
                    "Review pull request →",
                    type="primary",
                ):

                    try:

                        with st.spinner("Reviewing changes..."):

                            review = st.session_state.pilot.review_pr(
                                selected_pr
                            )

                        st.markdown("<hr>", unsafe_allow_html=True)

                        st.markdown(
                            '<div class="result-label">Review</div>',
                            unsafe_allow_html=True,
                        )

                        st.markdown(review)

                    except Exception as e:
                        st.error(str(e))

        except Exception as e:
            st.error(str(e))


# ============================================================
# TEST GENERATOR
# ============================================================

elif st.session_state.page == "Test Generator":

    section_heading("03", "Test Generator")

    st.markdown(
        """
        <div class="hero-subtitle">
            Generate suggested tests based on repository code and context.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.pilot:

        st.info("Analyze a repository first.")

    else:

        code_files = st.session_state.pilot.code_files

        if not code_files:

            st.warning("No supported code files were found.")

        else:

            selected_file = st.selectbox(
                "Target file",
                code_files,
            )

            if st.button(
                "Generate tests →",
                type="primary",
            ):

                try:

                    with st.spinner("Generating tests..."):

                        tests = st.session_state.pilot.generate_tests(
                            selected_file
                        )

                    st.markdown("<hr>", unsafe_allow_html=True)

                    st.markdown(
                        '<div class="result-label">Generated tests</div>',
                        unsafe_allow_html=True,
                    )

                    st.code(tests, language="python")

                    st.caption(
                        "Generated tests are suggestions. Review them before using them in production."
                    )

                except Exception as e:
                    st.error(str(e))


# ============================================================
# DOCS CHECK
# ============================================================

elif st.session_state.page == "Docs Check":

    section_heading("04", "Documentation Check")

    st.markdown(
        """
        <div class="hero-subtitle">
            Compare documentation with repository code and identify
            clear inconsistencies.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.pilot:

        st.info("Analyze a repository first.")

    else:

        if st.button(
            "Check documentation →",
            type="primary",
        ):

            try:

                with st.spinner("Checking documentation..."):

                    result = st.session_state.pilot.check_docs()

                st.markdown("<hr>", unsafe_allow_html=True)

                st.markdown(
                    '<div class="result-label">Documentation review</div>',
                    unsafe_allow_html=True,
                )

                st.markdown(result)

            except Exception as e:
                st.error(str(e))


# ============================================================
# FALLBACK
# ============================================================

else:

    st.session_state.page = "Overview"
    st.rerun()
