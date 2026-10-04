# ============================================================
# OVERVIEW — PREMIUM PRODUCT STYLE
# ============================================================

if st.session_state.page == "Overview":

    # --------------------------------------------------------
    # TOP BAR
    # --------------------------------------------------------

    if pilot:
        connection_text = f"●  {pilot.owner}/{pilot.repo}"
        connection_color = "#20FE6B"
    else:
        connection_text = "○  No repository connected"
        connection_color = "#777B90"

    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:5px 0 25px 0;
        ">

            <div style="
                color:#F9F9FD;
                font-size:13px;
                font-weight:600;
                letter-spacing:-0.01em;
            ">
                REPOPILOT
            </div>

            <div style="
                color:{connection_color};
                font-size:11px;
                font-weight:600;
                border:1px solid #1C2028;
                background:#0B0D12;
                padding:8px 12px;
                border-radius:100px;
            ">
                {connection_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            padding:45px 0 35px 0;
            max-width:950px;
        ">

            <div style="
                color:#20FE6B;
                font-size:10px;
                font-weight:700;
                letter-spacing:.18em;
                text-transform:uppercase;
                margin-bottom:20px;
            ">
                AI DEVELOPER WORKSPACE
            </div>

            <div style="
                color:#F9F9FD;
                font-size:clamp(44px, 6vw, 76px);
                line-height:.94;
                font-weight:800;
                letter-spacing:-.065em;
            ">
                Your repository.<br>

                <span style="color:#696D80;">
                    But intelligent.
                </span>
            </div>

            <div style="
                max-width:610px;
                color:#9296A9;
                font-size:14px;
                line-height:1.75;
                margin-top:25px;
            ">
                RepoPilot turns your GitHub codebase into an
                intelligent workspace for asking questions,
                reviewing pull requests, generating tests,
                and keeping documentation aligned.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # AI COMMAND BAR
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            margin:15px 0 30px 0;
            padding:5px;
            border:1px solid #292E38;
            background:#090B10;
            border-radius:15px;
            box-shadow:
                0 0 0 1px rgba(32,254,107,.025),
                0 20px 70px rgba(0,0,0,.30);
        ">
        """,
        unsafe_allow_html=True,
    )

    q_col, button_col = st.columns([6, 1])

    with q_col:

        overview_question = st.text_input(
            "AI command",
            placeholder="Ask anything about your repository...",
            label_visibility="collapsed",
            key="overview_question",
        )

    with button_col:

        ask_overview = st.button(
            "Ask  →",
            type="primary",
            use_container_width=True,
            key="overview_ask",
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # AI ANSWER
    # --------------------------------------------------------

    if ask_overview:

        if not pilot:

            st.warning(
                "Connect a GitHub repository from the sidebar first."
            )

        elif not overview_question.strip():

            st.warning(
                "Enter a question first."
            )

        else:

            with st.spinner(
                "RepoPilot is searching your codebase..."
            ):

                try:

                    answer, sources = pilot.answer(
                        overview_question.strip()
                    )

                    st.markdown(
                        """
                        <div style="
                            margin:0 0 30px 0;
                            padding:24px;
                            border:1px solid #1C2028;
                            border-radius:16px;
                            background:#0B0E13;
                        ">

                            <div style="
                                color:#20FE6B;
                                font-size:10px;
                                font-weight:700;
                                letter-spacing:.13em;
                                text-transform:uppercase;
                                margin-bottom:13px;
                            ">
                                REPOPILOT RESPONSE
                            </div>

                        """,
                        unsafe_allow_html=True,
                    )

                    st.markdown(answer)

                    render_sources(sources)

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True,
                    )

                except Exception as e:

                    st.error(str(e))

    # --------------------------------------------------------
    # STATS
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            margin-top:20px;
            margin-bottom:13px;
            color:#626678;
            font-size:10px;
            font-weight:700;
            letter-spacing:.14em;
            text-transform:uppercase;
        ">
            REPOSITORY SNAPSHOT
        </div>
        """,
        unsafe_allow_html=True,
    )

    if pilot:

        info = pilot.repo_info

        language = (
            ", ".join(info.get("languages", []))
            or "Unknown"
        )

        stats = [
            ("FILES", info.get("files", 0), "indexed"),
            ("CHUNKS", info.get("chunks", 0), "retrieval units"),
            ("STACK", language, "detected"),
            ("STATUS", "READY", "AI workspace"),
        ]

    else:

        stats = [
            ("FILES", "—", "connect repository"),
            ("CHUNKS", "—", "connect repository"),
            ("STACK", "—", "not detected"),
            ("STATUS", "OFFLINE", "waiting for repo"),
        ]

    stat_cols = st.columns(4)

    for col, (label, value, caption) in zip(
        stat_cols,
        stats,
    ):

        with col:

            st.markdown(
                f"""
                <div style="
                    padding:18px 2px;
                    border-top:1px solid #1C2028;
                    border-bottom:1px solid #1C2028;
                ">

                    <div style="
                        color:#626678;
                        font-size:9px;
                        font-weight:700;
                        letter-spacing:.14em;
                    ">
                        {label}
                    </div>

                    <div style="
                        color:#F9F9FD;
                        font-size:23px;
                        font-weight:700;
                        letter-spacing:-.04em;
                        margin-top:8px;
                    ">
                        {value}
                    </div>

                    <div style="
                        color:#5E6272;
                        font-size:10px;
                        margin-top:3px;
                    ">
                        {caption}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # LARGE FEATURE SECTION
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            margin-top:60px;
            margin-bottom:25px;
        ">

            <div style="
                color:#20FE6B;
                font-size:10px;
                font-weight:700;
                letter-spacing:.15em;
                text-transform:uppercase;
                margin-bottom:10px;
            ">
                THE WORKSPACE
            </div>

            <div style="
                color:#F9F9FD;
                font-size:32px;
                font-weight:750;
                letter-spacing:-.045em;
            ">
                Everything you need to<br>
                understand the code.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # FEATURE CARDS
    # --------------------------------------------------------

    feature_cols = st.columns([1.45, 1, 1])

    with feature_cols[0]:

        st.markdown(
            """
            <div style="
                min-height:270px;
                padding:25px;
                border:1px solid #1C2028;
                border-radius:17px;
                background:
                    radial-gradient(
                        circle at 85% 15%,
                        rgba(32,254,107,.08),
                        transparent 32%
                    ),
                    #0D1015;
                position:relative;
                overflow:hidden;
            ">

                <div style="
                    color:#20FE6B;
                    font-size:10px;
                    font-weight:700;
                    letter-spacing:.12em;
                ">
                    01  /  CODE INTELLIGENCE
                </div>

                <div style="
                    color:#F9F9FD;
                    font-size:25px;
                    font-weight:700;
                    letter-spacing:-.04em;
                    margin-top:22px;
                ">
                    Ask your<br>
                    codebase anything.
                </div>

                <div style="
                    color:#777B90;
                    font-size:12px;
                    line-height:1.65;
                    max-width:380px;
                    margin-top:15px;
                ">
                    Retrieve relevant files and get
                    concise answers grounded in actual
                    repository evidence.
                </div>

                <div style="
                    position:absolute;
                    right:25px;
                    bottom:22px;
                    color:#20FE6B;
                    font-size:24px;
                ">
                    ↗
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        if pilot:

            if st.button(
                "Open Code Q&A  →",
                use_container_width=True,
                key="overview_codeqa",
            ):

                go_to("Code Q&A")
                st.rerun()

    with feature_cols[1]:

        st.markdown(
            """
            <div style="
                min-height:270px;
                padding:25px;
                border:1px solid #1C2028;
                border-radius:17px;
                background:#0D1015;
            ">

                <div style="
                    color:#28B1DC;
                    font-size:10px;
                    font-weight:700;
                    letter-spacing:.12em;
                ">
                    02  /  REVIEW
                </div>

                <div style="
                    color:#F9F9FD;
                    font-size:21px;
                    font-weight:700;
                    letter-spacing:-.035em;
                    margin-top:22px;
                ">
                    PR review<br>
                    with context.
                </div>

                <div style="
                    color:#777B90;
                    font-size:11px;
                    line-height:1.65;
                    margin-top:15px;
                ">
                    Understand changes against
                    the surrounding codebase.
                </div>

                <div style="
                    color:#28B1DC;
                    font-size:22px;
                    margin-top:55px;
                ">
                    ⌘
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        if pilot:

            if st.button(
                "Open PR Review  →",
                use_container_width=True,
                key="overview_pr",
            ):

                go_to("PR Review")
                st.rerun()

    with feature_cols[2]:

        st.markdown(
            """
            <div style="
                min-height:270px;
                padding:25px;
                border:1px solid #1C2028;
                border-radius:17px;
                background:#0D1015;
            ">

                <div style="
                    color:#9B8CFF;
                    font-size:10px;
                    font-weight:700;
                    letter-spacing:.12em;
                ">
                    03  /  AUTOMATE
                </div>

                <div style="
                    color:#F9F9FD;
                    font-size:21px;
                    font-weight:700;
                    letter-spacing:-.035em;
                    margin-top:22px;
                ">
                    Tests & docs.<br>
                    Generated.
                </div>

                <div style="
                    color:#777B90;
                    font-size:11px;
                    line-height:1.65;
                    margin-top:15px;
                ">
                    Generate test suggestions and
                    identify documentation gaps.
                </div>

                <div style="
                    color:#9B8CFF;
                    font-size:22px;
                    margin-top:55px;
                ">
                    ◇
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        if pilot:

            if st.button(
                "Explore Tools  →",
                use_container_width=True,
                key="overview_tools",
            ):

                go_to("Test Generator")
                st.rerun()

    # --------------------------------------------------------
    # REPOSITORY STRUCTURE
    # --------------------------------------------------------

    if pilot:

        st.markdown(
            """
            <div style="
                margin-top:60px;
                margin-bottom:22px;
            ">

                <div style="
                    color:#626678;
                    font-size:10px;
                    font-weight:700;
                    letter-spacing:.14em;
                    text-transform:uppercase;
                ">
                    REPOSITORY
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        structure_left, structure_right = st.columns(
            [1.4, 1]
        )

        with structure_left:

            st.markdown(
                f"""
                <div style="
                    padding:24px;
                    border:1px solid #1C2028;
                    border-radius:16px;
                    background:#0B0E13;
                ">

                    <div style="
                        color:#F9F9FD;
                        font-size:16px;
                        font-weight:650;
                    ">
                        {pilot.owner}/{pilot.repo}
                    </div>

                    <div style="
                        color:#626678;
                        font-size:11px;
                        margin-top:6px;
                    ">
                        Branch · {info.get("branch", "main")}
                    </div>

                    <div style="
                        height:1px;
                        background:#1C2028;
                        margin:20px 0;
                    ">
                    </div>

                    <div style="
                        color:#626678;
                        font-size:9px;
                        font-weight:700;
                        letter-spacing:.13em;
                        margin-bottom:10px;
                    ">
                        KEY DIRECTORIES
                    </div>

                """,
                unsafe_allow_html=True,
            )

            directories = info.get(
                "directories",
                [],
            )

            if directories:

                for directory in directories[:10]:

                    st.markdown(
                        f"""
                        <div style="
                            padding:8px 0;
                            color:#AEB2C5;
                            font-size:12px;
                            border-bottom:1px solid #151820;
                        ">
                            <span style="
                                color:#20FE6B;
                                margin-right:8px;
                            ">
                                /
                            </span>
                            {directory}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            else:

                st.caption(
                    "No top-level directories detected."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

        with structure_right:

            st.markdown(
                """
                <div style="
                    padding:24px;
                    border:1px solid #1C2028;
                    border-radius:16px;
                    background:#0B0E13;
                ">

                    <div style="
                        color:#F9F9FD;
                        font-size:16px;
                        font-weight:650;
                    ">
                        Test coverage signals
                    </div>

                    <div style="
                        color:#626678;
                        font-size:11px;
                        margin-top:6px;
                    ">
                        Files detected by RepoPilot
                    </div>

                    <div style="
                        height:1px;
                        background:#1C2028;
                        margin:20px 0;
                    ">
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
                        f"""
                        <div style="
                            padding:8px 0;
                            color:#AEB2C5;
                            font-size:11px;
                            font-family:ui-monospace,
                            SFMono-Regular,Menlo,monospace;
                            border-bottom:1px solid #151820;
                        ">
                            {test}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            else:

                st.caption(
                    "No obvious test files detected."
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # FINAL CTA
    # --------------------------------------------------------

    if not pilot:

        st.markdown(
            """
            <div style="
                margin-top:70px;
                padding:45px;
                text-align:center;
                border:1px solid #1C2028;
                border-radius:18px;
                background:
                    radial-gradient(
                        circle at 50% 0%,
                        rgba(32,254,107,.07),
                        transparent 45%
                    ),
                    #090B10;
            ">

                <div style="
                    color:#F9F9FD;
                    font-size:28px;
                    font-weight:750;
                    letter-spacing:-.04em;
                ">
                    Your codebase is waiting.
                </div>

                <div style="
                    color:#777B90;
                    font-size:12px;
                    margin-top:10px;
                ">
                    Connect a GitHub repository from the sidebar
                    to start exploring.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# CODE Q&A
# ============================================================
