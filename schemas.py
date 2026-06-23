from pydantic import BaseModel
from typing import Dict, Any, Literal


class AgentDecision(BaseModel):

    action: Literal[
        "get_weather",
        "save_memory",
        "get_memory",
        "create_note",
        "final"
    ]

    args: Dict[str, Any] = {}

    answer: str | None = None