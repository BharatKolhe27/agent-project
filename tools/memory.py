import json


MEMORY_FILE = "memory.json"


def save_memory(key: str, value: str):

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