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
    """
    Create and save a note.

    Use when the user wants something
    written down for later reference.

    Trigger phrases:

    - Create a note
    - Save a note
    - Write this down
    - Take a note
    - Remember this note

    Examples:

    User:
    Create a note saying learn LangGraph.

    User:
    Write down buy groceries tomorrow.

    User:
    Save a note about project ideas.

    Required Arguments:

    text:
        Note content.

    Returns:

    {
        "status": "success",
        "message": "note created"
    }
    """
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