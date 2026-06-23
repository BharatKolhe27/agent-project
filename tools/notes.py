import json
import os


NOTES_FILE = "notes.json"


if not os.path.exists(
    NOTES_FILE
):

    with open(
        NOTES_FILE,
        "w"
    ) as f:

        json.dump([], f)


def create_note(text: str):

    if not text:

        return {
            "status": "error",
            "message": "note text required"
        }

    with open(
        NOTES_FILE,
        "r"
    ) as f:

        notes = json.load(f)

    notes.append(text)

    with open(
        NOTES_FILE,
        "w"
    ) as f:

        json.dump(
            notes,
            f,
            indent=2
        )

    return {
        "status": "success",
        "message": "note created"
    }