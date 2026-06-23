from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from schemas import AgentDecision
from system_prompt import SYSTEM_PROMPT


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

planner = llm.with_structured_output(
    AgentDecision
)


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