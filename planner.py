from dotenv import load_dotenv
load_dotenv()

import os
import json

from langchain_openai import ChatOpenAI

from schemas import AgentDecision
from system_prompt import SYSTEM_PROMPT


llm = ChatOpenAI(
    model="openai/gpt-oss-120b:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    ),
    temperature=0
)


def plan(messages):

    history = "\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in messages
        ]
    )

    prompt = f"""
{SYSTEM_PROMPT}

Conversation:

{history}
"""

    response = llm.invoke(
        prompt
    )

    print("\nRAW RESPONSE:")
    print(response.content)

    for attempt in range(3):

        response = llm.invoke(
            prompt
        )

        print(
            "\nRAW RESPONSE:"
        )
        print(
            response.content
        )

        try:

            data = json.loads(
                response.content
            )
            if (
                data.get("action") == "final"
                and "args" in data
                and "answer" in data["args"]
            ):
             data["answer"] = data["args"]["answer"]

            return AgentDecision(
                **data
            )

        except Exception as e:

            print(
                f"\nPlanner Retry "
                f"{attempt + 1}: {e}"
            )

            prompt += f"""

    The previous response was invalid.

    Error:
    {e}

    Return valid JSON.
    Use only valid actions.
    """