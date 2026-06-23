from tools.weather import get_weather

from tools.memory import (
    save_memory,
    get_memory
)

from tools.notes import (
    create_note
)

TOOLS = {
    "get_weather": get_weather,
    "save_memory": save_memory,
    "get_memory": get_memory,
    "create_note": create_note
}


def execute_action(
    action,
    args
):

    return TOOLS[action](
        **args
    )