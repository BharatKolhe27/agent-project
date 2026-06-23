from agent import (
    structured_llm,
    SYSTEM_PROMPT
)

response = structured_llm.invoke(
    f"""
{SYSTEM_PROMPT}

User:
Remember my favorite language
is Spanish.
"""
)

print(response)
print(type(response))