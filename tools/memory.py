import json


MEMORY_FILE = "memory.json"


def save_memory(key: str, value: str):
    """
    Save user information permanently.

    Use when user says:

    - Remember this
    - Save this
    - Don't forget
    - My favorite ...
    - Store this information

    Examples:

    User:
    Remember my favorite language is Spanish

    User:
    Save my favorite city as Pune
    """

    if not key or not value:

        return {
            "status": "error",
            "message": "key and value required"
        }

    with open(
        MEMORY_FILE,
        "r"
    ) as f:

        data = json.load(f)

    data[key] = value

    with open(
        MEMORY_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )

    return {
        "status": "success",
        "message": f"saved {key}"
    }


def get_memory(key: str):
    """
    Retrieve previously saved user information.

    Use when user asks:

    - What is my ...
    - What's my ...
    - Do you remember ...
    - What did I tell you ...
    - Favorite ...

    Examples:

    User:
    What is my favorite language?

    User:
    Do you remember my favorite city?
    """
    with open(
        MEMORY_FILE,
        "r"
    ) as f:

        data = json.load(f)

    if key not in data:

        return {
            "status": "error",
            "message": "memory not found"
        }

    return {
        "status": "success",
        "value": data[key]
    }