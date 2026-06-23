from dotenv import load_dotenv

load_dotenv()

import time

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from schemas import AgentDecision

from tools.weather import get_weather

from tools.memory import (
    save_memory,
    get_memory
)

from tools.notes import (
    create_note
)


# -------------------
# LLM
# -------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

planner = llm.with_structured_output(
    AgentDecision
)


# -------------------
# TOOLS
# -------------------

TOOLS = {
    "get_weather": get_weather,
    "save_memory": save_memory,
    "get_memory": get_memory,
    "create_note": create_note
}


# -------------------
# SYSTEM PROMPT
# -------------------
SYSTEM_PROMPT = """
You are a personal assistant.

Available tools:

get_weather(city)
- Get weather.

save_memory(key,value)
- Save user information.

get_memory(key)
- Retrieve saved information.

create_note(text)
- Save notes.

IMPORTANT:

If the user asks:

- What is my ...
- Do you remember ...
- What did I tell you ...
- What is my favorite ...

ALWAYS call get_memory first.

Never answer memory questions directly.

Use tools whenever information might exist.

Only use final when you have enough information.
"""

# -------------------
# PLANNER
# -------------------

def plan(messages):

    history = "\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in messages
        ]
    )

    return planner.invoke(
        f"""
{SYSTEM_PROMPT}

Conversation:

{history}
"""
    )


# -------------------
# VALIDATOR
# -------------------

def validate_action(
    action,
    args
):

    if action == "get_weather":

        return "city" in args

    if action == "save_memory":

        return (
            "key" in args
            and
            "value" in args
        )

    if action == "get_memory":

        return "key" in args

    if action == "create_note":

        return "text" in args

    return True


# -------------------
# EXECUTOR
# -------------------

def execute_action(
    action,
    args
):

    return TOOLS[action](
        **args
    )


# -------------------
# AGENT LOOP
# -------------------

def run_agent(
    question,
    max_steps=5
):

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    trace = []

    for step in range(max_steps):

        decision = plan(
            messages
        )

        print(
            f"\nSTEP {step}"
        )

        print(
            decision
        )

        if decision.action == "final":

            return {
                "answer":
                    decision.answer,
                "trace":
                    trace
            }

        if decision.action not in TOOLS:

            return {
                "answer":
                    f"Unknown tool "
                    f"{decision.action}",
                "trace":
                    trace
            }

        if not validate_action(
            decision.action,
            decision.args
        ):

            return {
                "answer":
                    "Validation failed",
                "trace":
                    trace
            }

        start = time.time()

        result = execute_action(
            decision.action,
            decision.args
        )

        latency = (
            time.time() - start
        )

        trace.append(
            {
                "step": step,
                "reasoning":
                    decision.reasoning,
                "tool":
                    decision.action,
                "args":
                    decision.args,
                "result":
                    result,
                "latency":
                    round(
                        latency,
                        3
                    )
            }
        )

        messages.append(
            {
                "role":
                    "assistant",
                "content":
                    str(decision)
            }
        )

        messages.append(
            {
                "role":
                    "tool",
                "content":
                    str(result)
            }
        )

    return {
        "answer":
            "Max steps reached",
        "trace":
            trace
    }