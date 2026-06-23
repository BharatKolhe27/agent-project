import time
import streamlit as st

from stream_agent import stream_agent

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Agent Studio",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.block-container {
    padding-top: 1rem;
    max-width: 1400px;
}

.user-msg {
    padding: 14px;
    border-radius: 12px;
    background: #eff6ff;
    margin-bottom: 10px;
    border-left: 4px solid #2563eb;
}

.agent-msg {
    padding: 14px;
    border-radius: 12px;
    background: #f9fafb;
    margin-bottom: 10px;
    border-left: 4px solid #10b981;
}

.timeline-card {
    padding: 12px;
    border-radius: 10px;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    margin-bottom: 10px;
}

.final-answer {
    padding: 18px;
    border-radius: 12px;
    background: #ecfdf5;
    border: 1px solid #10b981;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "runs" not in st.session_state:
    st.session_state.runs = []

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🤖 Agent Studio")

st.caption(
    "Planner • Tool Calling • Observability • Streaming"
)

st.divider()

# --------------------------------------------------
# INPUT
# --------------------------------------------------

question = st.text_area(
    "Ask your Agent",
    height=120,
    placeholder="What's the weather in Indore and save it as a note?"
)

run = st.button(
    "🚀 Run Agent",
    use_container_width=True
)

# --------------------------------------------------
# METRICS ROW
# --------------------------------------------------

metrics_placeholder = st.empty()

st.markdown("---")

# --------------------------------------------------
# MAIN LAYOUT
# --------------------------------------------------

left, right = st.columns(
    [2, 1]
)

# --------------------------------------------------
# CHAT
# --------------------------------------------------

with left:

    st.subheader("💬 Conversation")

    conversation_placeholder = st.empty()

    st.markdown("---")

    st.subheader("🎯 Final Answer")

    answer_placeholder = st.empty()

# --------------------------------------------------
# TIMELINE
# --------------------------------------------------

with right:

    st.subheader("⚡ Agent Timeline")

    timeline_placeholder = st.empty()

# --------------------------------------------------
# EXECUTION
# --------------------------------------------------

if run and question:

    start_time = time.time()

    llm_calls = 0
    tool_calls = 0
    steps = 0

    answer = ""

    timeline = []

    tool_usage = {}

    conversation_placeholder.markdown(
        f"""
<div class="user-msg">
<b>You</b><br>
{question}
</div>
        """,
        unsafe_allow_html=True
    )

    for event in stream_agent(question):

        runtime = round(
            time.time() - start_time,
            2
        )

        # --------------------------------
        # STATUS
        # --------------------------------

        if event["type"] == "status":

            timeline.append(
                f"⚡ {event['message']}"
            )

        # --------------------------------
        # PLANNER
        # --------------------------------

        elif event["type"] == "planner":

            llm_calls += 1
            steps += 1

            timeline.append(
                f"🧠 Planner → {event['action']}"
            )

        # --------------------------------
        # TOOL
        # --------------------------------

        elif event["type"] == "tool":

            tool_calls += 1

            tool_name = event["tool"]

            tool_usage[
                tool_name
            ] = tool_usage.get(
                tool_name,
                0
            ) + 1

            timeline.append(
                f"🔧 Tool → {tool_name}"
            )

            timeline.append(
                f"📄 Observation"
            )

        # --------------------------------
        # FINAL
        # --------------------------------

        elif event["type"] == "final":

            answer = event["answer"]

            answer_placeholder.markdown(
                f"""
<div class="final-answer">
{answer}
</div>
                """,
                unsafe_allow_html=True
            )

            conversation_placeholder.markdown(
                f"""
<div class="user-msg">
<b>You</b><br>
{question}
</div>

<div class="agent-msg">
<b>Agent</b><br>
{answer}
</div>
                """,
                unsafe_allow_html=True
            )

            timeline.append(
                "✅ Final Answer"
            )

        # --------------------------------
        # METRICS
        # --------------------------------

        with metrics_placeholder.container():

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "LLM Calls",
                llm_calls
            )

            c2.metric(
                "Tool Calls",
                tool_calls
            )

            c3.metric(
                "Steps",
                steps
            )

            c4.metric(
                "Runtime",
                f"{runtime}s"
            )

        # --------------------------------
        # TIMELINE
        # --------------------------------

        with timeline_placeholder.container():

            for item in timeline:

                if item.startswith("🧠"):

                    st.info(item)

                elif item.startswith("🔧"):

                    st.success(item)

                elif item.startswith("📄"):

                    st.warning(item)

                elif item.startswith("⚡"):

                    st.write(item)

                elif item.startswith("✅"):

                    st.success(item)

        time.sleep(0.15)

    # --------------------------------
    # SAVE RUN
    # --------------------------------

    st.session_state.runs.append(
        {
            "question": question,
            "answer": answer,
            "runtime": runtime,
            "llm_calls": llm_calls,
            "tool_calls": tool_calls
        }
    )

# --------------------------------------------------
# RUN HISTORY
# --------------------------------------------------

if st.session_state.runs:

    st.markdown("---")

    with st.expander(
        "📚 Previous Runs",
        expanded=False
    ):

        for run in reversed(
            st.session_state.runs
        ):

            st.markdown(
                f"""
**Question**

{run['question']}

**Answer**

{run['answer']}

---
"""
            )