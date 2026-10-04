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
# LIGHT PREMIUM UI
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: "Inter", sans-serif;
    }

    .stApp {
        background: #F7F8FA;
        color: #15171A;
    }

    .main .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E7E9ED;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.25rem;
    }

    .brand {
        padding: 0.2rem 0.25rem 1.8rem 0.25rem;
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-mark {
        width: 35px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: #E9F9EF;
        border: 1px solid #C9F0D6;
        color: #159447;
        font-size: 18px;
        font-weight: 800;
    }

    .brand-name {
        font-size: 18px;
        font-weight: 800;
        color: #16181C;
        letter-spacing: -0.5px;
    }

    .brand-sub {
        color: #8A909A;
        font-size: 11px;
        margin-top: 6px;
        padding-left: 45px;
    }

    .sidebar-section {
        color: #9AA0AA;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin: 1.25rem 0 0.55rem 0;
    }

    /* ========================================================
       SIDEBAR BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 9px;
        border: 1px solid transparent;
        background: transparent;
        color: #68707C;
        font-weight: 500;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        background: #F4F6F8;
        border-color: #E5E8EC;
        color: #17191D;
    }

    .stButton button[kind="primary"] {
        background: #18A957 !important;
        border: 1px solid #18A957 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    .stButton button[kind="primary"]:hover {
        background: #12964B !important;
        border-color: #12964B !important;
    }

    /* ========================================================
       SIDEBAR INPUTS
       ======================================================== */

    section[data-testid="stSidebar"] input {
        background: #F8F9FA !important;
        border: 1px solid #E1E4E8 !important;
        color: #202328 !important;
        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"] input:focus {
        border-color: #72C994 !important;
        box-shadow: 0 0 0 2px rgba(24, 169, 87, 0.08) !important;
    }

    /* ========================================================
       TOP BAR
       ======================================================== */

    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.4rem;
    }

    .breadcrumb {
        color: #8B919B;
        font-size: 12px;
    }

    .breadcrumb strong {
        color: #34383F;
    }

    .connected-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: #ECF9F0;
        color: #158947;
        border: 1px solid #D1F0DA;
        border-radius: 999px;
        padding: 6px 10px;
        font-size: 11px;
        font-weight: 600;
    }

    .connected-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #1AAF59;
    }

    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        position: relative;
        background: #FFFFFF;
        border: 1px solid #E5E8EC;
        border-radius: 20px;
        padding: 3.4rem 3.5rem;
        overflow: hidden;
        margin-bottom: 1.3rem;
        box-shadow: 0 8px 35px rgba(26, 32, 44, 0.035);
    }

    .hero::after {
        content: "";
        position: absolute;
        right: -120px;
        top: -150px;
        width: 350px;
        height: 350px;
        border-radius: 50%;
        background: rgba(36, 185, 98, 0.055);
        border: 1px solid rgba(36, 185, 98, 0.09);
    }

    .eyebrow {
        color: #159447;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .hero-title {
        color: #111318;
        font-size: clamp(38px, 5vw, 66px);
        line-height: 1;
        letter-spacing: -3px;
        font-weight: 800;
        margin: 0;
        max-width: 850px;
    }

    .hero-title span {
        color: #9AA0AA;
    }

    .hero-description {
        max-width: 680px;
        color: #707782;
        font-size: 15px;
        line-height: 1.7;
        margin-top: 1.35rem;
    }

    .hero-mini {
        position: relative;
        z-index: 2;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-top: 1.7rem;
        padding: 9px 13px;
        background: #F7F9F8;
        border: 1px solid #DCEFE2;
        border-radius: 9px;
        color: #5F6863;
        font-size: 11px;
    }

    .hero-mini-icon {
        color: #18A957;
        font-weight: 700;
    }

    /* ========================================================
       SECTION HEADINGS
       ======================================================== */

    .section-label {
        color: #969CA6;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin: 1.5rem 0 0.7rem 0;
    }

    .section-title {
        color: #17191D;
        font-size: 21px;
        font-weight: 750;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
    }

    .section-description {
        color: #858B95;
        font-size: 12px;
        margin-bottom: 1rem;
    }

    /* ========================================================
       METRIC CARDS
       ======================================================== */

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E5E8EC;
        border-radius: 13px;
        padding: 1.2rem;
        min-height: 108px;
        box-shadow: 0 4px 18px rgba(26, 32, 44, 0.025);
    }

    .metric-number {
        color: #17191D;
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .metric-label {
        color: #8B919B;
        font-size: 11px;
        margin-top: 5px;
    }

    .metric-accent {
        width: 25px;
        height: 3px;
        background: #1AAF59;
        border-radius: 99px;
        margin-bottom: 11px;
    }

    /* ========================================================
       FEATURE CARDS
       ======================================================== */

    .feature-card {
        background: #FFFFFF;
        border: 1px solid #E5E8EC;
        border-radius: 14px;
        padding: 1.25rem;
        min-height: 175px;
        box-shadow: 0 4px 18px rgba(26, 32, 44, 0.025);
        transition: all 0.15s ease;
    }

    .feature-card:hover {
        border-color: #C9D0D8;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(26, 32, 44, 0.06);
    }

    .feature-icon {
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: #EDF9F1;
        border: 1px solid #D6F0DE;
        color: #159447;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 1rem;
    }

    .feature-title {
        color: #1B1E23;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 0.45rem;
    }

    .feature-description {
        color: #7C838D;
        font-size: 12px;
        line-height: 1.6;
    }

    /* ========================================================
       DETAIL CARDS
       ======================================================== */

    .detail-card {
        background: #FFFFFF;
        border: 1px solid #E5E8EC;
        border-radius: 12px;
        padding: 1.1rem;
        min-height: 82px;
        box-shadow: 0 3px 15px rgba(26, 32, 44, 0.02);
    }

    .detail-title {
        color: #969CA6;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
    }

    .detail-value {
        color: #353A42;
        font-size: 13px;
        line-height: 1.5;
        word-break: break-word;
    }

    /* ========================================================
       STATUS
       ======================================================== */

    .status-ready {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        color: #168F49;
        font-size: 11px;
        font-weight: 600;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #1AAF59;
    }

    .status-neutral {
        color: #9AA0AA;
        font-size: 11px;
    }

    /* ========================================================
       FORM ELEMENTS
       ======================================================== */

    input,
    textarea {
        background-color: #FFFFFF !important;
        color: #202328 !important;
        border-color: #DDE1E6 !important;
    }

    textarea {
        border-radius: 10px !important;
    }

    input:focus,
    textarea:focus {
        border-color: #72C994 !important;
        box-shadow: 0 0 0 2px rgba(24, 169, 87, 0.08) !important;
    }

    /* ========================================================
       TABS
       ======================================================== */

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid #E5E8EC;
    }

    .stTabs [data-baseweb="tab"] {
        color: #7C838D;
        padding: 9px 13px;
    }

    .stTabs [aria-selected="true"] {
        color: #159447 !important;
    }

    /* ========================================================
       CODE
       ======================================================== */

    pre {
        background: #F8F9FA !important;
        border: 1px solid #E2E5E9 !important;
        border-radius: 10px !important;
    }

    code {
        color: #126E39 !important;
    }

    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {
        border-color: #E7E9ED !important;
    }

    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;
        color: #A0A5AE;
        font-size: 10px;
        margin-top: 3rem;
        padding-top: 1.4rem;
        border-top: 1px solid #E5E8EC;
    }

    /* ========================================================
       MOBILE
       ======================================================== */

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

    st.markdown(
        '<div class="section-label">Sources</div>',
        unsafe_allow_html=True,
    )

    for source in sources:

        st.markdown(
            f"""
            <div class="detail-card" style="margin-bottom:8px;">
                <div class="detail-value">
                    ◈ {source}
                </div>
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
                background:#EDF9F1;
                border:1px solid #D4EEDF;
                border-radius:9px;
                padding:9px 12px;
                color:#158947;
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

            <div class="brand-row">
                <div class="brand-mark">◈</div>
                <div class="brand-name">RepoPilot</div>
            </div>

            <div class="brand-sub">
                AI developer workspace
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section">Workspace</div>',
        unsafe_allow_html=True,
    )

    page_button("Overview", "Overview", "⌂")
    page_button("Code Q&A", "Code Q&A", "⌘")
    page_button("PR Review", "PR Review", "↗")
    page_button("Test Generator", "Test Generator", "✓")
    page_button("Docs Check", "Docs Check", "≡")

    st.markdown(
        '<div class="sidebar-section">Repository</div>',
        unsafe_allow_html=True,
    )

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

            st.error(
                "Enter a GitHub repository URL."
            )

        else:

            try:

                with st.spinner(
                    "Analyzing repository..."
                ):

                    pilot = RepoPilot(
                        repo_url.strip(),
                        groq_key.strip() or None,
                    )

                    pilot.build_index()

                    st.session_state.pilot = pilot
                    st.session_state.repo_url = repo_url.strip()
                    st.session_state.analysis_error = ""

                st.success(
                    "Repository analyzed successfully."
                )

                st.rerun()

            except Exception as e:

                st.session_state.analysis_error = str(e)

                st.error(
                    f"Could not analyze repository: {e}"
                )

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

        st.caption(
            f"{pilot.owner}/{pilot.repo}"
        )

    else:

        st.markdown(
            """
            <div class="status-neutral">
                ● No repository connected
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# TOP BAR
# ============================================================

pilot = get_pilot()

repo_name = (
    f"{pilot.owner}/{pilot.repo}"
    if pilot
    else "No repository"
)

st.markdown(
    f"""
    <div class="topbar">

        <div class="breadcrumb">
            RepoPilot&nbsp;&nbsp;/&nbsp;&nbsp;
            <strong>{st.session_state.page}</strong>
        </div>

        <div>
            {
                '<div class="connected-pill">'
                '<span class="connected-dot"></span>'
                + repo_name +
                '</div>'
                if pilot
                else
                '<div class="breadcrumb">Connect a repository to begin</div>'
            }
        </div>

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

            <div class="eyebrow">
                AI Developer Workspace
            </div>

            <h1 class="hero-title">
                Understand your codebase.<br>
                <span>Ship with confidence.</span>
            </h1>

            <div class="hero-description">
                RepoPilot is your AI teammate for GitHub.
                Analyze repositories, ask questions about your code,
                review pull requests, generate tests, and keep
                documentation consistent — all from one workspace.
            </div>

            <div class="hero-mini">
                <span class="hero-mini-icon">✦</span>
                Connect a repository from the sidebar to get started
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if pilot:

        info = pilot.repo_info

        # ----------------------------------------------------
        # SNAPSHOT
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label">Repository snapshot</div>',
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-accent"></div>
                    <div class="metric-number">
                        {info.get("files", 0)}
                    </div>
                    <div class="metric-label">
                        Files indexed
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-accent"></div>
                    <div class="metric-number">
                        {info.get("chunks", 0)}
                    </div>
                    <div class="metric-label">
                        Knowledge chunks
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:

            languages = info.get(
                "languages",
                [],
            )

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-accent"></div>
                    <div class="metric-number">
                        {len(languages)}
                    </div>
                    <div class="metric-label">
                        Languages detected
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c4:

            st.markdown(
                """
                <div class="metric-card">
                    <div class="metric-accent"></div>
                    <div class="metric-number">
                        Ready
                    </div>
                    <div class="metric-label">
                        Workspace status
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ----------------------------------------------------
        # FEATURES
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label">AI tools</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-title">Everything you need to work with a repo</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-description">One workspace for understanding, reviewing, testing, and maintaining your code.</div>',
            unsafe_allow_html=True,
        )

        f1, f2, f3, f4 = st.columns(4)

        feature_data = [
            (
                f1,
                "⌘",
                "Code Q&A",
                "Ask questions about architecture, functions, files, and implementation details.",
            ),
            (
                f2,
                "↗",
                "PR Review",
                "Review pull requests and surface evidence-based issues and recommendations.",
            ),
            (
                f3,
                "✓",
                "Test Generator",
                "Generate practical test suggestions using your repository's existing context.",
            ),
            (
                f4,
                "≡",
                "Docs Check",
                "Compare documentation against code and identify clear inconsistencies.",
            ),
        ]

        for column, icon, title, description in feature_data:

            with column:

                st.markdown(
                    f"""
                    <div class="feature-card">

                        <div class="feature-icon">
                            {icon}
                        </div>

                        <div class="feature-title">
                            {title}
                        </div>

                        <div class="feature-description">
                            {description}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # ----------------------------------------------------
        # REPOSITORY DETAILS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label">Repository details</div>',
            unsafe_allow_html=True,
        )

        d1, d2, d3 = st.columns(3)

        with d1:

            st.markdown(
                f"""
                <div class="detail-card">

                    <div class="detail-title">
                        Repository
                    </div>

                    <div class="detail-value">
                        {info.get("name", "Unknown")}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        with d2:

            languages_text = ", ".join(
                info.get("languages", [])
            )

            if not languages_text:
                languages_text = "Not detected"

            st.markdown(
                f"""
                <div class="detail-card">

                    <div class="detail-title">
                        Languages
                    </div>

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

                    <div class="detail-title">
                        Default branch
                    </div>

                    <div class="detail-value">
                        {info.get("branch", "Unknown")}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        # ----------------------------------------------------
        # DIRECTORIES
        # ----------------------------------------------------

        directories = info.get(
            "directories",
            [],
        )

        if directories:

            st.markdown(
                '<div class="section-label">Key directories</div>',
                unsafe_allow_html=True,
            )

            directory_columns = st.columns(4)

            for i, directory in enumerate(
                directories[:8]
            ):

                with directory_columns[i % 4]:

                    st.markdown(
                        f"""
                        <div class="detail-card"
                             style="margin-bottom:10px;">

                            <div class="detail-value">
                                / {directory}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # ----------------------------------------------------
        # TESTS + DOCS
        # ----------------------------------------------------

        test_files = info.get(
            "tests",
            [],
        )

        doc_files = info.get(
            "docs",
            [],
        )

        if test_files or doc_files:

            st.markdown(
                '<div class="section-label">Repository health</div>',
                unsafe_allow_html=True,
            )

            h1, h2 = st.columns(2)

            with h1:

                st.markdown(
                    f"""
                    <div class="detail-card">

                        <div class="detail-title">
                            Test files detected
                        </div>

                        <div class="detail-value">
                            {len(test_files)}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with h2:

                st.markdown(
                    f"""
                    <div class="detail-card">

                        <div class="detail-title">
                            Documentation files
                        </div>

                        <div class="detail-value">
                            {len(doc_files)}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    else:

        # ----------------------------------------------------
        # EMPTY STATE
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label">Get started</div>',
            unsafe_allow_html=True,
        )

        e1, e2 = st.columns([1.5, 1])

        with e1:

            st.markdown(
                """
                <div class="detail-card"
                     style="min-height:180px;">

                    <div class="detail-title">
                        Connect your repository
                    </div>

                    <div class="detail-value">

                        Enter a public GitHub repository URL
                        in the sidebar and click
                        <b>Analyze Repository</b>.

                        <br><br>

                        RepoPilot will fetch the repository,
                        build a searchable index, and prepare
                        your AI developer workspace.

                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        with e2:

            st.markdown(
                """
                <div class="detail-card"
                     style="min-height:180px;">

                    <div class="detail-title">
                        Workflow
                    </div>

                    <div class="detail-value">

                        <b>01</b> Connect<br>
                        <b>02</b> Analyze<br>
                        <b>03</b> Index<br>
                        <b>04</b> Ask & Assist

                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# CODE Q&A
# ============================================================

elif st.session_state.page == "Code Q&A":

    pilot = get_pilot()

    st.markdown(
        """
        <div class="section-label">Repository intelligence</div>

        <div class="section-title">
            Codebase Q&A
        </div>

        <div class="section-description">
            Ask questions and get answers grounded in your indexed repository.
        </div>
        """,
        unsafe_allow_html=True,
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
            height=140,
        )

        if st.button(
            "Ask RepoPilot",
            type="primary",
        ):

            if not question.strip():

                st.warning(
                    "Enter a question first."
                )

            else:

                with st.spinner(
                    "Searching the codebase..."
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

                        st.error(
                            f"Could not answer the question: {e}"
                        )


# ============================================================
# PR REVIEW
# ============================================================

elif st.session_state.page == "PR Review":

    pilot = get_pilot()

    st.markdown(
        """
        <div class="section-label">Code quality</div>

        <div class="section-title">
            Pull Request Review
        </div>

        <div class="section-description">
            Review open pull requests using repository context.
        </div>
        """,
        unsafe_allow_html=True,
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
                <div class="detail-card"
                     style="margin-top:12px;">

                    <div class="detail-title">
                        Pull Request
                    </div>

                    <div class="detail-value">
                        #{selected_pr["number"]}
                        ·
                        {selected_pr["title"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            if selected_pr.get("body"):

                with st.expander(
                    "View PR description"
                ):

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

                        st.markdown(
                            "### Review"
                        )

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

    st.markdown(
        """
        <div class="section-label">Developer productivity</div>

        <div class="section-title">
            Test Generator
        </div>

        <div class="section-description">
            Generate test suggestions based on your repository's code and context.
        </div>
        """,
        unsafe_allow_html=True,
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

    st.markdown(
        """
        <div class="section-label">Documentation quality</div>

        <div class="section-title">
            Documentation Check
        </div>

        <div class="section-description">
            Compare repository documentation with the actual code.
        </div>
        """,
        unsafe_allow_html=True,
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
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        RepoPilot&nbsp;&nbsp;·&nbsp;&nbsp;
        AI teammate for GitHub repositories
    </div>
    """,
    unsafe_allow_html=True,
)
