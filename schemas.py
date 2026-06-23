from pydantic import BaseModel, Field
from typing import Dict, Any, Literal


class AgentDecision(BaseModel):

    action: Literal[
        "get_weather",
        "save_memory",
        "get_memory",
        "create_note",
        "final"
    ]

    args: Dict[str, Any] = Field(default_factory=dict)

    answer: str = ""

    reasoning: str = ""