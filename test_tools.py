from tools.weather import get_weather
from tools.memory import (
    save_memory,
    get_memory
)
from tools.notes import (
    create_note
)

print(
    get_weather("Pune")
)

print(
    save_memory(
        "favorite_language",
        "Spanish"
    )
)

print(
    get_memory(
        "favorite_language"
    )
)

print(
    create_note(
        "Learn LangGraph"
    )
)