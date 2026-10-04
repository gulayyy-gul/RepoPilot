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
# PREMIUM DARK UI
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #040308;
    --sidebar: #08090D;
    --card: #0D1015;
    --card-hover: #12161D;
    --text: #F9F9FD;
    --muted: #9C9EB4;
    --border: #1C2028;
    --green: #20FE6B;
    --blue: #28B1DC;
    --purple: #4C5EAF;
}

html,
body,
[class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(32, 254, 107, 0.055),
            transparent 26%
        ),
        radial-gradient(
            circle at 55% 45%,
            rgba(76, 94, 175, 0.035),
            transparent 32%
        ),
        var(--bg);
    color: var(--text);
}

/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background: var(--sidebar);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem;
}

.brand {
    padding: 0.4rem 0.4rem 1.7rem;
}

.brand-mark {
    display: inline-flex;
    width: 40px;
    height: 40px;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: linear-gradient(
        135deg,
        rgba(32, 254, 107, 0.18),
        rgba(40, 177, 220, 0.10)
    );
    border: 1px solid rgba(32, 254, 107, 0.28);
    color: var(--green);
    font-size: 21px;
    font-weight: 800;
    margin-right: 9px;
}

.brand-name {
    color: var(--text);
    font-size: 21px;
    font-weight: 800;
    vertical-align: middle;
    letter-spacing: -0.03em;
}

.brand-sub {
    color: #74788D;
    font-size: 11px;
    line-height: 1.55;
    margin-top: 9px;
}

.nav-label {
    color: #626678;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    font-size: 10px;
    font-weight: 700;
    margin: 1.2rem 0 0.55rem;
}

.repo-pill {
    padding: 11px 13px;
    border: 1px solid var(--border);
    background: #0B0D12;
    border-radius: 12px;
    margin-bottom: 15px;
}

.repo-title {
    color: var(--text);
    font-size: 12px;
    font-weight: 600;
    overflow-wrap: anywhere;
}

.repo-status {
    color: var(--green);
    font-size: 10px;
    margin-top: 5px;
}

/* ============================================================
   MAIN AREA
   ============================================================ */

.block-container {
    max-width: 1450px;
    padding: 2rem 3rem 4rem;
}

h1,
h2,
h3 {
    color: var(--text) !important;
    letter-spacing: -0.035em;
}

h1 {
    font-size: 2.7rem !important;
    font-weight: 800 !important;
}

h2 {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}

h3 {
    font-size: 1.1rem !important;
    font-weight: 700 !important;
}

p {
    color: var(--muted);
}

/* ============================================================
   HERO
   ============================================================ */

.hero {
    padding: 2.3rem 2.4rem;
    border: 1px solid var(--border);
    border-radius: 18px;

    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(32, 254, 107, 0.085),
            transparent 28%
        ),
        linear-gradient(
            145deg,
            rgba(13, 16, 21, 0.98),
            rgba(7, 9, 13, 0.98)
        );

    box-shadow: 0 18px 70px rgba(0, 0, 0, 0.28);

    margin-bottom: 1.3rem;
}

.eyebrow {
    color: var(--green);
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    margin-bottom: 10px;
}

.hero-title {
    color: var(--text);
    font-size: 38px;
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: -0.05em;
    margin-bottom: 13px;
}

.hero-copy {
    color: #A2A5B8;
    max-width: 720px;
    line-height: 1.7;
    font-size: 13px;
}

/* ============================================================
   CARDS
   ============================================================ */

.card {
    border: 1px solid var(--border);
    background: rgba(13, 16, 21, 0.88);
    border-radius: 15px;
    padding: 18px;
    min-height: 105px;
    margin-bottom: 12px;
}

.card-title {
    color: #777B90;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.11em;
    font-weight: 700;
}

.card-value {
    color: var(--text);
    font-size: 27px;
    font-weight: 750;
    margin-top: 8px;
}

.card-caption {
    color: #6E7284;
    font-size: 10px;
    margin-top: 4px;
}

.section-title {
    color: var(--text);
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin: 1.5rem 0 0.8rem;
}

/* ============================================================
   COMMAND CENTER
   ============================================================ */

.command {
    border: 1px solid rgba(32, 254, 107, 0.18);
    background:
        radial-gradient(
            circle at 90% 0%,
            rgba(32, 254, 107, 0.08),
            transparent 30%
        ),
        #0A0D12;

    border-radius: 16px;
    padding: 19px;
    margin: 8px 0 15px;
}

.command-label {
    color: var(--green);
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 7px;
}

/* ============================================================
   INPUTS
   ============================================================ */

.stTextInput > div > div,
.stTextArea > div > div,
.stSelectbox > div > div {
    background: #0B0E13 !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
}

input,
textarea {
    color: var(--text) !important;
}

.stTextInput label,
.stTextArea label,
.stSelectbox label {
    color: #8C90A4 !important;
}

/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 9px;
    border: 1px solid var(--border);
    background: #10131A;
    color: #EDEEF5;
    font-weight: 600;
    transition: 0.15s ease;
}

.stButton > button:hover {
    border-color: rgba(32, 254, 107, 0.4);
    color: var(--green);
    background: #111720;
}

.stButton > button[kind="primary"] {
    background: var(--green);
    color: #031006;
    border-color: var(--green);
    font-weight: 800;
}

.stButton > button[kind="primary"]:hover {
    background: #5CFF91;
    color: #031006;
}

/* ============================================================
   INFO BOX
   ============================================================ */

.info-box {
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 14px 16px;
    background: #0A0C11;
    color: #9296A9;
    font-size: 12px;
    line-height: 1.65;
}

/* ============================================================
   METRICS
   ============================================================ */

[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 15px !important;
}

[data-testid="stMetricLabel"] {
    color: #777B90 !important;
}

[data-testid="stMetricValue"] {
    color: var(--text) !important;
}

/* ============================================================
   SOURCE PILLS
   ============================================================ */

.source {
    display: inline-block;
    padding: 5px 9px;
    margin: 3px 5px 3px 0;
    border-radius: 7px;
    background: #11151C;
    border: 1px solid var(--border);
    color: #AEB2C5;
    font-size: 10px;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}

/* ============================================================
   EXPANDERS
   ============================================================ */

[data-testid="stExpander"] {
    background: #0B0E13;
    border: 1px solid var(--border);
    border-radius: 12px;
}

/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    color: #555A6C;
    font-size: 10px;
    text-align: center;
}

hr {
    border-color: var(--border);
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "pilot" not in st.session_state:
    st.session_state.pilot = None

if "page" not in st.session_state:
    st.session_state.page = "Overview"

pilot = st.session_state.pilot


# ============================================================
# HELPERS
# ============================================================

def go_to(page):
    st.session_state.page = page


def render_sources(sources):
    if not sources:
        return

    html = ""

    for source in sources:
        html += f'<span class="source">{source}</span>'

    st.markdown(
        f"""
        <div style="margin-top:15px;">
            <div style="
                color:#626678;
                font-size:10px;
                font-weight:700;
                letter-spacing:.12em;
                margin-bottom:5px;
            ">
                SOURCES
            </div>
            {html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <span class="brand-mark">◈</span>
            <span class="brand-name">RepoPilot</span>

            <div class="brand-sub">
                AI teammate for your GitHub repository
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Repository status

    if pilot:

        st.markdown(
            f"""
            <div class="repo-pill">
                <div class="repo-title">
                    ⌘ {pilot.owner}/{pilot.repo}
                </div>

                <div class="repo-status">
                    ● Indexed & ready
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <div class="repo-pill">
                <div class="repo-title">
                    No repository connected
                </div>

                <div class="repo-status" style="color:#626678;">
                    Connect a repository below
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Navigation

    st.markdown(
        '<div class="nav-label">Workspace</div>',
        unsafe_allow_html=True,
    )

    pages = [
        ("Overview", "⌂"),
        ("Code Q&A", "◌"),
        ("PR Review", "⌘"),
        ("Test Generator", "◇"),
        ("Docs Check", "▤"),
    ]

    for page_name, icon in pages:

        if st.button(
            f"{icon}  {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.page == page_name
                else "secondary"
            ),
        ):
            go_to(page_name)
            st.rerun()

    # Repository connection

    st.markdown(
        '<div class="nav-label">Repository</div>',
        unsafe_allow_html=True,
    )

    repo_url = st.text_input(
        "GitHub repository",
        placeholder="https://github.com/owner/repo",
        label_visibility="collapsed",
    )

    groq_key = st.text_input(
        "Groq API key",
        placeholder="Groq API key",
        type="password",
        label_visibility="collapsed",
    )

    if st.button(
        "Analyze Repository",
        type="primary",
        use_container_width=True,
    ):

        if not repo_url.strip():

            st.error("Enter a GitHub repository URL.")

        else:

            with st.spinner("Analyzing repository..."):

                try:

                    new_pilot = RepoPilot(
                        repo_url.strip(),
                        groq_key.strip() or None,
                    )

                    info = new_pilot.build_index()

                    st.session_state.pilot = new_pilot
                    st.session_state.page = "Overview"

                    st.success("Repository indexed.")
                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Could not analyze repository: {e}"
                    )

    st.markdown(
        """
        <div class="info-box">

        <b style="color:#AEB2C5;">Read-only MVP</b><br><br>

        RepoPilot analyzes repository evidence and provides
        advisory AI assistance.

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE HEADER
# ============================================================

if pilot:

    st.caption(
        f"WORKSPACE  /  {pilot.owner}/{pilot.repo}"
    )

else:

    st.caption(
        "WORKSPACE  /  REPOSITORY NOT CONNECTED"
    )


# ============================================================
# OVERVIEW
# ============================================================

if st.session_state.page == "Overview":

    st.markdown(
        """
        <div class="hero">

            <div class="eyebrow">
                AI Developer Workspace
            </div>

            <div class="hero-title">
                Understand your codebase.<br>
                Move faster.
            </div>

            <div class="hero-copy">
                RepoPilot analyzes your GitHub repository,
                retrieves relevant code, and turns it into
                practical answers, reviews, tests, and
                documentation insights.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ----------------------------------------
    # No repository
    # ----------------------------------------

    if not pilot:

        st.markdown(
            '<div class="section-title">Connect your repository</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="info-box">

            Use the sidebar to connect a public GitHub repository.

            Once indexed, RepoPilot unlocks:

            <b style="color:#F9F9FD;">
            Code Q&A · PR Review · Test Generator · Docs Check
            </b>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-title">What RepoPilot can do</div>',
            unsafe_allow_html=True,
        )

        cols = st.columns(4)

        features = [
            (
                "Code Q&A",
                "Ask questions and get evidence-backed answers.",
            ),
            (
                "PR Review",
                "Review open pull requests for meaningful issues.",
            ),
            (
                "Test Generator",
                "Generate suggested tests from repository code.",
            ),
            (
                "Docs Check",
                "Find clear documentation inconsistencies.",
            ),
        ]

        for col, (title, description) in zip(cols, features):

            with col:

                st.markdown(
                    f"""
                    <div class="card">

                        <div class="card-title">
                            {title}
                        </div>

                        <div style="
                            color:#A2A5B8;
                            font-size:12px;
                            line-height:1.6;
                            margin-top:9px;
                        ">
                            {description}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ----------------------------------------
    # Connected repository
    # ----------------------------------------

    else:

        info = pilot.repo_info

        st.markdown(
            '<div class="section-title">Repository Overview</div>',
            unsafe_allow_html=True,
        )

        cols = st.columns(4)

        statistics = [
            (
                "Files",
                info.get("files", 0),
                "indexed files",
            ),
            (
                "Chunks",
                info.get("chunks", 0),
                "RAG chunks",
            ),
            (
                "Language",
                ", ".join(
                    info.get("languages", [])
                ) or "Unknown",
                "detected",
            ),
            (
                "Status",
                "Ready",
                "AI workspace",
            ),
        ]

        for col, (label, value, caption) in zip(
            cols,
            statistics,
        ):

            with col:

                st.markdown(
                    f"""
                    <div class="card">

                        <div class="card-title">
                            {label}
                        </div>

                        <div class="card-value">
                            {value}
                        </div>

                        <div class="card-caption">
                            {caption}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # ----------------------------------------
        # Command center
        # ----------------------------------------

        st.markdown(
            '<div class="section-title">AI Command Center</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="command">

                <div class="command-label">
                    Ask RepoPilot
                </div>

                <div style="
                    color:#8F93A7;
                    font-size:12px;
                    line-height:1.6;
                ">

                    Ask anything about the indexed repository.
                    RepoPilot retrieves relevant evidence before
                    generating an answer.

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        question = st.text_input(
            "Repository question",
            placeholder=(
                "e.g. How is authentication handled "
                "in this repository?"
            ),
            label_visibility="collapsed",
        )

        if st.button(
            "Ask RepoPilot  →",
            type="primary",
        ):

            if not question.strip():

                st.warning(
                    "Enter a question first."
                )

            else:

                with st.spinner(
                    "Searching repository evidence..."
                ):

                    try:

                        answer, sources = pilot.answer(
                            question.strip()
                        )

                        st.markdown(
                            "### RepoPilot"
                        )

                        st.markdown(answer)

                        render_sources(
                            sources
                        )

                    except Exception as e:

                        st.error(str(e))

        # ----------------------------------------
        # Repository structure
        # ----------------------------------------

        st.markdown(
            '<div class="section-title">Repository structure</div>',
            unsafe_allow_html=True,
        )

        left, right = st.columns(2)

        with left:

            st.markdown(
                """
                <div class="card">

                    <div class="card-title">
                        Key directories
                    </div>

                """,
                unsafe_allow_html=True,
            )

            directories = info.get(
                "directories",
                [],
            )

            if directories:

                for directory in directories:

                    st.markdown(
                        f"`{directory}/`"
                    )

            else:

                st.caption(
                    "No top-level directories detected."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

        with right:

            st.markdown(
                """
                <div class="card">

                    <div class="card-title">
                        Tests detected
                    </div>

                """,
                unsafe_allow_html=True,
            )

            tests = info.get(
                "tests",
                [],
            )

            if tests:

                for test in tests[:8]:

                    st.markdown(
                        f"`{test}`"
                    )

            else:

                st.caption(
                    "No obvious test files detected."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


# ============================================================
# CODE Q&A
# ============================================================

elif st.session_state.page == "Code Q&A":

    st.markdown(
        """
        <div class="hero">

            <div class="eyebrow">
                Repository Intelligence
            </div>

            <div class="hero-title">
                Talk to your codebase.
            </div>

            <div class="hero-copy">
                Ask natural-language questions.
                RepoPilot retrieves relevant repository
                evidence before generating the answer.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if not pilot:

        st.info(
            "Connect a repository from the sidebar first."
        )

    else:

        question = st.text_area(
            "Question",
            placeholder=(
                "How does this repository handle "
                "HTTP requests?"
            ),
            height=130,
        )

        if st.button(
            "Ask RepoPilot",
            type="primary",
        ):

            if not question.strip():

                st.warning(
                    "Enter a question."
                )

            else:

                with st.spinner(
                    "Retrieving relevant code..."
                ):

                    try:

                        answer, sources = pilot.answer(
                            question.strip()
                        )

                        st.markdown(
                            "### Answer"
                        )

                        st.markdown(answer)

                        render_sources(
                            sources
                        )

                    except Exception as e:

                        st.error(str(e))


# ============================================================
# PR REVIEW
# ============================================================

elif st.session_state.page == "PR Review":

    st.markdown(
        """
        <div class="hero">

            <div class="eyebrow">
                Code Review
            </div>

            <div class="hero-title">
                Review pull requests<br>
                with context.
            </div>

            <div class="hero-copy">
                RepoPilot combines the PR diff with related
                repository code and returns evidence-based
                review findings.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if not pilot:

        st.info(
            "Connect a repository from the sidebar first."
        )

    else:

        try:

            prs = pilot.list_pull_requests()

        except Exception as e:

            prs = []

            st.error(str(e))

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
                "Open pull request",
                list(options.keys()),
            )

            pr = options[selected]

            with st.expander(
                "Pull request description",
                expanded=False,
            ):

                st.write(
                    pr.get("body")
                    or "No description provided."
                )

            if st.button(
                "Review Pull Request",
                type="primary",
            ):

                with st.spinner(
                    "Reviewing PR diff against repository context..."
                ):

                    try:

                        review = pilot.review_pr(
                            pr
                        )

                        st.markdown(
                            "### Review findings"
                        )

                        st.markdown(review)

                    except Exception as e:

                        st.error(str(e))


# ============================================================
# TEST GENERATOR
# ============================================================

elif st.session_state.page == "Test Generator":

    st.markdown(
        """
        <div class="hero">

            <div class="eyebrow">
                Test Generation
            </div>

            <div class="hero-title">
                Turn repository code<br>
                into tests.
            </div>

            <div class="hero-copy">
                Select an indexed code file and generate
                a test suggestion based on its source and
                nearby repository context.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if not pilot:

        st.info(
            "Connect a repository from the sidebar first."
        )

    elif not pilot.code_files:

        st.warning(
            "No supported code files were detected."
        )

    else:

        path = st.selectbox(
            "Target file",
            pilot.code_files,
        )

        if st.button(
            "Generate Tests",
            type="primary",
        ):

            with st.spinner(
                "Generating test suggestion..."
            ):

                try:

                    tests = pilot.generate_tests(
                        path
                    )

                    st.markdown(
                        "### Suggested tests"
                    )

                    st.code(
                        tests,
                        language="python",
                    )

                    st.caption(
                        "Review and adapt generated tests "
                        "to the repository's actual framework "
                        "and conventions."
                    )

                except Exception as e:

                    st.error(str(e))


# ============================================================
# DOCUMENTATION CHECK
# ============================================================

elif st.session_state.page == "Docs Check":

    st.markdown(
        """
        <div class="hero">

            <div class="eyebrow">
                Documentation Health
            </div>

            <div class="hero-title">
                Keep docs aligned<br>
                with code.
            </div>

            <div class="hero-copy">
                RepoPilot compares documentation with
                repository code and reports clear,
                evidence-based inconsistencies.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if not pilot:

        st.info(
            "Connect a repository from the sidebar first."
        )

    else:

        docs = pilot.repo_info.get(
            "docs",
            [],
        )

        code_files = pilot.code_files

        left, right = st.columns(2)

        with left:

            st.markdown(
                f"""
                <div class="card">

                    <div class="card-title">
                        Documentation files
                    </div>

                    <div class="card-value">
                        {len(docs)}
                    </div>

                    <div class="card-caption">
                        detected in repository
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        with right:

            st.markdown(
                f"""
                <div class="card">

                    <div class="card-title">
                        Code files
                    </div>

                    <div class="card-value">
                        {len(code_files)}
                    </div>

                    <div class="card-caption">
                        available for comparison
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        if docs:

            with st.expander(
                "Detected documentation",
                expanded=False,
            ):

                for document in docs:

                    st.markdown(
                        f"`{document}`"
                    )

        if st.button(
            "Run Documentation Check",
            type="primary",
        ):

            with st.spinner(
                "Checking documentation against repository evidence..."
            ):

                try:

                    result = pilot.check_docs()

                    st.markdown(
                        "### Documentation review"
                    )

                    st.markdown(result)

                except Exception as e:

                    st.error(str(e))


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        RepoPilot · AI teammate for GitHub repositories
        · Read-only advisory MVP
    </div>
    """,
    unsafe_allow_html=True,
)
