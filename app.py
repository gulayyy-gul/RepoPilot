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

if "page" not in st.session_state:
    st.session_state.page = "Overview"

if "pilot" not in st.session_state:
    st.session_state.pilot = None

if "repo_url" not in st.session_state:
    st.session_state.repo_url = ""

if "groq_key" not in st.session_state:
    st.session_state.groq_key = ""

if "analysis_error" not in st.session_state:
    st.session_state.analysis_error = ""


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: "Inter", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 75% 5%,
                rgba(32, 254, 107, 0.055),
                transparent 28%
            ),
            radial-gradient(
                circle at 20% 45%,
                rgba(76, 94, 175, 0.045),
                transparent 30%
            ),
            #040308;
        color: #F9F9FD;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #08090D;
        border-right: 1px solid #1C2028;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.2rem;
    }

    .brand {
        padding: 0.3rem 0.2rem 1.8rem 0.2rem;
    }

    .brand-mark {
        display: inline-flex;
        width: 34px;
        height: 34px;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: rgba(32, 254, 107, 0.10);
        border: 1px solid rgba(32, 254, 107, 0.28);
        color: #20FE6B;
        font-size: 18px;
        font-weight: 800;
        margin-right: 9px;
    }

    .brand-name {
        font-size: 18px;
        font-weight: 800;
        letter-spacing: -0.5px;
        vertical-align: middle;
    }

    .brand-sub {
        color: #777B8D;
        font-size: 11px;
        margin-top: 5px;
        padding-left: 44px;
    }

    .sidebar-section {
        color: #666A7B;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        margin: 1.3rem 0 0.55rem 0;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid transparent;
        background: transparent;
        color: #A9ACBC;
        font-weight: 500;
        text-align: left;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        background: #12161D;
        border-color: #1C2028;
        color: #F9F9FD;
    }

    /* ---------- SIDEBAR INPUT ---------- */

    section[data-testid="stSidebar"] input {
        background: #0D1015 !important;
        border: 1px solid #1C2028 !important;
        color: #F9F9FD !important;
        border-radius: 9px !important;
    }

    section[data-testid="stSidebar"] input:focus {
        border-color: rgba(32, 254, 107, 0.45) !important;
        box-shadow: 0 0 0 1px rgba(32, 254, 107, 0.15) !important;
    }

    /* ---------- HERO ---------- */

    .hero {
        position: relative;
        padding: 3.5rem 3.5rem 3rem 3.5rem;
        border: 1px solid #1C2028;
        border-radius: 22px;
        background:
            radial-gradient(
                circle at 80% 25%,
                rgba(32, 254, 107, 0.10),
                transparent 26%
            ),
            radial-gradient(
                circle at 95% 85%,
                rgba(76, 94, 175, 0.10),
                transparent 25%
            ),
            #0A0C11;
        overflow: hidden;
        margin-bottom: 1.2rem;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        right: -130px;
        top: -140px;
        border-radius: 50%;
        border: 1px solid rgba(32, 254, 107, 0.10);
        box-shadow:
            0 0 0 40px rgba(32, 254, 107, 0.025),
            0 0 0 80px rgba(32, 254, 107, 0.015);
    }

    .eyebrow {
        display: inline-block;
        color: #20FE6B;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin-bottom: 1.1rem;
    }

    .hero-title {
        font-size: clamp(38px, 5vw, 68px);
        line-height: 0.98;
        letter-spacing: -3px;
        font-weight: 800;
        max-width: 800px;
        margin: 0;
    }

    .hero-title span {
        color: #777B8D;
    }

    .hero-description {
        max-width: 650px;
        color: #999DAD;
        font-size: 15px;
        line-height: 1.7;
        margin-top: 1.4rem;
    }

    /* ---------- COMMAND BAR ---------- */

    .command {
        margin-top: 2rem;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 15px;
        border: 1px solid #292E38;
        background: #080A0E;
        border-radius: 12px;
        max-width: 670px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.22);
    }

    .command-icon {
        color: #20FE6B;
        font-size: 17px;
    }

    .command-text {
        color: #777B8D;
        font-size: 13px;
    }

    .command-key {
        margin-left: auto;
        color: #606575;
        border: 1px solid #252933;
        background: #101219;
        border-radius: 6px;
        padding: 4px 7px;
        font-size: 10px;
    }

    /* ---------- SECTION ---------- */

    .section-label {
        color: #666A7B;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin: 1.5rem 0 0.7rem 0;
    }

    /* ---------- CARDS ---------- */

    .metric-card,
    .feature-card,
    .detail-card {
        background: #0D1015;
        border: 1px solid #1C2028;
        border-radius: 15px;
        padding: 1.15rem;
        height: 100%;
        transition: border-color 0.15s ease, transform 0.15s ease;
    }

    .metric-card:hover,
    .feature-card:hover,
    .detail-card:hover {
        border-color: #303641;
        transform: translateY(-1px);
    }

    .metric-number {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .metric-label {
        color: #707484;
        font-size: 11px;
        margin-top: 4px;
    }

    .feature-icon {
        width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 9px;
        background: rgba(32, 254, 107, 0.08);
        border: 1px solid rgba(32, 254, 107, 0.18);
        color: #20FE6B;
        font-weight: 700;
        margin-bottom: 0.9rem;
    }

    .feature-title {
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    .feature-description {
        color: #777B8D;
        font-size: 12px;
        line-height: 1.55;
    }

    .detail-title {
        color: #666A7B;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .detail-value {
        color: #E7E8EE;
        font-size: 13px;
        line-height: 1.5;
        word-break: break-word;
    }

    /* ---------- STATUS ---------- */

    .status-ready {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        color: #20FE6B;
        font-size: 11px;
        font-weight: 600;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        background: #20FE6B;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(32,254,107,0.55);
    }

    .status-neutral {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        color: #8A8E9E;
        font-size: 11px;
    }

    /* ---------- INPUTS ---------- */

    input,
    textarea {
        background-color: #0D1015 !important;
        color: #F9F9FD !important;
        border-color: #1C2028 !important;
    }

    textarea {
        border-radius: 11px !important;
    }

    /* ---------- PRIMARY BUTTON ---------- */

    .stButton button[kind="primary"] {
        background: #20FE6B !important;
        color: #031008 !important;
        border: none !important;
        font-weight: 700 !important;
    }

    .stButton button[kind="primary"]:hover {
        background: #43ff83 !important;
        color: #031008 !important;
    }

    /* ---------- TABS ---------- */

    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        color: #777B8D;
        border-radius: 8px;
        padding: 8px 13px;
    }

    .stTabs [aria-selected="true"] {
        color: #F9F9FD !important;
        background: #11141A;
    }

    /* ---------- CODE ---------- */

    code {
        color: #B8FFC9 !important;
    }

    pre {
        border: 1px solid #1C2028 !important;
        border-radius: 12px !important;
    }

    /* ---------- DIVIDER ---------- */

    hr {
        border-color: #1C2028 !important;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #4F5362;
        font-size: 10px;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #151820;
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 900px) {

        .hero {
            padding: 2rem;
        }

        .hero-title {
            font-size: 42px;
            letter-spacing: -2px;
        }

        .main .block-container {
            padding: 1rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def get_pilot():
    return st.session_state.get("pilot")


def render_sources(sources):
    if not sources:
        return

    st.markdown("### Sources")

    for source in sources:
        st.markdown(
            f"""
            <div class="detail-card" style="margin-bottom:8px;">
                <div class="detail-value">◈ {source}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def page_button(label, page_name, icon):
    active = st.session_state.page == page_name

    if active:
        st.markdown(
            f"""
            <div style="
                background:#12161D;
                border:1px solid #252B34;
                border-radius:10px;
                padding:9px 12px;
                color:#F9F9FD;
                font-size:13px;
                font-weight:600;
                margin-bottom:4px;
            ">
                {icon}&nbsp;&nbsp;{label}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        if st.button(
            f"{icon}  {label}",
            key=f"nav_{page_name}",
            use_container_width=True,
        ):
            st.session_state.page = page_name
            st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div>
                <span class="brand-mark">◈</span>
                <span class="brand-name">RepoPilot</span>
            </div>
            <div class="brand-sub">AI developer workspace</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section">Workspace</div>', unsafe_allow_html=True)

    page_button("Overview", "Overview", "⌂")
    page_button("Code Q&A", "Code Q&A", "⌘")
    page_button("PR Review", "PR Review", "↗")
    page_button("Test Generator", "Test Generator", "✓")
    page_button("Docs Check", "Docs Check", "≡")

    st.markdown('<div class="sidebar-section">Repository</div>', unsafe_allow_html=True)

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
        "Analyze Repository",
        type="primary",
        use_container_width=True,
    ):

        if not repo_url.strip():
            st.error("Enter a GitHub repository URL.")

        else:
            try:
                with st.spinner("Analyzing repository..."):

                    pilot = RepoPilot(
                        repo_url.strip(),
                        groq_key.strip() or None,
                    )

                    pilot.build_index()

                    st.session_state.pilot = pilot
                    st.session_state.repo_url = repo_url.strip()
                    st.session_state.analysis_error = ""

                st.success("Repository analyzed successfully.")
                st.rerun()

            except Exception as e:
                st.session_state.analysis_error = str(e)
                st.error(f"Could not analyze repository: {e}")

    pilot = get_pilot()

    if pilot:
        st.markdown("---")

        st.markdown(
            """
            <div class="status-ready">
                <span class="status-dot"></span>
                Repository ready
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption(f"{pilot.owner}/{pilot.repo}")

    else:
        st.markdown(
            """
            <div class="status-neutral">
                <span>●</span>
                No repository connected
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# OVERVIEW
# ============================================================

if st.session_state.page == "Overview":

    pilot = get_pilot()

    st.markdown(
        """
        <div class="hero">

            <div class="eyebrow">AI Developer Workspace</div>

            <h1 class="hero-title">
                Your repository.<br>
                <span>But intelligent.</span>
            </h1>

            <div class="hero-description">
                RepoPilot understands your codebase, answers technical
                questions, reviews pull requests, generates tests,
                and checks your documentation — all from one workspace.
            </div>

            <div class="command">
                <div class="command-icon">⌕</div>
                <div class="command-text">
                    Ask anything about your repository...
                </div>
                <div class="command-key">AI</div>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if pilot:

        info = pilot.repo_info

        st.markdown(
            '<div class="section-label">Repository snapshot</div>',
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">{info.get("files", 0)}</div>
                    <div class="metric-label">Files indexed</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">{info.get("chunks", 0)}</div>
                    <div class="metric-label">Knowledge chunks</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:
            languages = info.get("languages", [])

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">{len(languages)}</div>
                    <div class="metric-label">Languages detected</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c4:
            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-number">Ready</div>
                    <div class="metric-label">Workspace status</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="section-label">What RepoPilot can do</div>',
            unsafe_allow_html=True,
        )

        f1, f2, f3 = st.columns(3)

        features = [
            (
                f1,
                "⌘",
                "Codebase Q&A",
                "Ask questions about architecture, functions, files, and implementation details.",
            ),
            (
                f2,
                "↗",
                "PR Review",
                "Inspect pull requests and surface evidence-based issues and recommendations.",
            ),
            (
                f3,
                "✓",
                "Test Generator",
                "Generate practical test suggestions using the repository's existing context.",
            ),
            (
                f1,
                "≡",
                "Docs Check",
                "Compare documentation against code and identify clear inconsistencies.",
            ),
        ]

        for index, (column, icon, title, description) in enumerate(features):

            if index == 3:
                st.markdown("<br>", unsafe_allow_html=True)

            with column:
                st.markdown(
                    f"""
                    <div class="feature-card">
                        <div class="feature-icon">{icon}</div>
                        <div class="feature-title">{title}</div>
                        <div class="feature-description">
                            {description}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown(
            '<div class="section-label">Repository details</div>',
            unsafe_allow_html=True,
        )

        d1, d2, d3 = st.columns(3)

        with d1:
            st.markdown(
                f"""
                <div class="detail-card">
                    <div class="detail-title">Repository</div>
                    <div class="detail-value">
                        {info.get("name", "Unknown")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with d2:
            languages_text = ", ".join(info.get("languages", []))
            if not languages_text:
                languages_text = "Not detected"

            st.markdown(
                f"""
                <div class="detail-card">
                    <div class="detail-title">Languages</div>
                    <div class="detail-value">
                        {languages_text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with d3:
            st.markdown(
                f"""
                <div class="detail-card">
                    <div class="detail-title">Default branch</div>
                    <div class="detail-value">
                        {info.get("branch", "Unknown")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="section-label">Key directories</div>',
            unsafe_allow_html=True,
        )

        directories = info.get("directories", [])

        if directories:

            cols = st.columns(min(4, max(1, len(directories))))

            for i, directory in enumerate(directories[:8]):

                with cols[i % len(cols)]:
                    st.markdown(
                        f"""
                        <div class="detail-card">
                            <div class="detail-value">
                                / {directory}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        st.markdown(
            """
            <div class="footer">
                RepoPilot · AI teammate for GitHub repositories
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <div class="section-label">Get started</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="detail-card">

                <div class="detail-title">
                    Connect your repository
                </div>

                <div class="detail-value">
                    Enter a public GitHub repository in the sidebar
                    and click <b>Analyze Repository</b>.
                    RepoPilot will index the repository and prepare
                    the AI workspace.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="footer">
                RepoPilot · Connect → Analyze → Index → Assist
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# CODE Q&A
# ============================================================

elif st.session_state.page == "Code Q&A":

    pilot = get_pilot()

    st.title("Code Q&A")

    st.caption(
        "Ask questions about the indexed repository."
    )

    if not pilot:

        st.warning(
            "Connect and analyze a repository first."
        )

    else:

        question = st.text_area(
            "Question",
            placeholder=(
                "Example: Where is authentication handled?\n"
                "Example: How are requests retried?\n"
                "Example: What is the purpose of the main module?"
            ),
            height=130,
        )

        if st.button(
            "Ask RepoPilot",
            type="primary",
        ):

            if not question.strip():

                st.warning("Enter a question first.")

            else:

                with st.spinner("Searching the codebase..."):

                    try:

                        answer, sources = pilot.answer(
                            question.strip()
                        )

                        st.markdown("### Answer")

                        st.markdown(answer)

                        render_sources(sources)

                    except Exception as e:

                        st.error(
                            f"Could not answer the question: {e}"
                        )


# ============================================================
# PR REVIEW
# ============================================================

elif st.session_state.page == "PR Review":

    pilot = get_pilot()

    st.title("PR Review")

    st.caption(
        "Review open pull requests using repository context."
    )

    if not pilot:

        st.warning(
            "Connect and analyze a repository first."
        )

    else:

        try:

            prs = pilot.list_pull_requests()

        except Exception as e:

            prs = []
            st.error(
                f"Could not load pull requests: {e}"
            )

        if not prs:

            st.info(
                "No open pull requests were found."
            )

        else:

            options = {
                f"#{pr['number']} — {pr['title']}": pr
                for pr in prs
            }

            selected = st.selectbox(
                "Select pull request",
                list(options.keys()),
            )

            selected_pr = options[selected]

            st.markdown(
                f"""
                <div class="detail-card">
                    <div class="detail-title">
                        Pull Request
                    </div>
                    <div class="detail-value">
                        #{selected_pr["number"]} ·
                        {selected_pr["title"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if selected_pr.get("body"):

                with st.expander("PR description"):

                    st.write(
                        selected_pr["body"]
                    )

            if st.button(
                "Review Pull Request",
                type="primary",
            ):

                with st.spinner(
                    "Reviewing pull request..."
                ):

                    try:

                        result = pilot.review_pr(
                            selected_pr
                        )

                        st.markdown("### Review")

                        st.markdown(result)

                    except Exception as e:

                        st.error(
                            f"Could not review PR: {e}"
                        )


# ============================================================
# TEST GENERATOR
# ============================================================

elif st.session_state.page == "Test Generator":

    pilot = get_pilot()

    st.title("Test Generator")

    st.caption(
        "Generate test suggestions using the repository's context."
    )

    if not pilot:

        st.warning(
            "Connect and analyze a repository first."
        )

    else:

        code_files = pilot.code_files

        if not code_files:

            st.info(
                "No supported code files were found."
            )

        else:

            selected_file = st.selectbox(
                "Select a source file",
                code_files,
            )

            if st.button(
                "Generate Tests",
                type="primary",
            ):

                with st.spinner(
                    "Generating tests..."
                ):

                    try:

                        tests = pilot.generate_tests(
                            selected_file
                        )

                        st.markdown(
                            "### Generated Tests"
                        )

                        st.code(
                            tests,
                            language="python",
                        )

                        st.caption(
                            "Generated tests are suggestions. "
                            "Review and adjust them before using "
                            "them in the project."
                        )

                    except Exception as e:

                        st.error(
                            f"Could not generate tests: {e}"
                        )


# ============================================================
# DOCS CHECK
# ============================================================

elif st.session_state.page == "Docs Check":

    pilot = get_pilot()

    st.title("Documentation Check")

    st.caption(
        "Compare documentation with the indexed repository code."
    )

    if not pilot:

        st.warning(
            "Connect and analyze a repository first."
        )

    else:

        docs = pilot.repo_info.get(
            "docs",
            [],
        )

        if docs:

            st.markdown(
                "### Documentation files"
            )

            for doc in docs:

                st.markdown(
                    f"""
                    <div class="detail-card"
                         style="margin-bottom:8px;">
                        <div class="detail-value">
                            ≡ {doc}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        else:

            st.info(
                "No documentation files were detected."
            )

        st.markdown("---")

        if st.button(
            "Check Documentation",
            type="primary",
        ):

            with st.spinner(
                "Checking documentation..."
            ):

                try:

                    result = pilot.check_docs()

                    st.markdown(
                        "### Documentation Review"
                    )

                    st.markdown(result)

                except Exception as e:

                    st.error(
                        f"Could not check documentation: {e}"
                    )


# ============================================================
# FALLBACK
# ============================================================

else:

    st.session_state.page = "Overview"
    st.rerun()
