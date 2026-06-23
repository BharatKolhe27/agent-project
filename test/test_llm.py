from planner import llm
from system_prompt import SYSTEM_PROMPT

response = llm.invoke(
    f"""
{SYSTEM_PROMPT}

User:
Remember my favorite language is Spanish.
"""
)

print(response.content)