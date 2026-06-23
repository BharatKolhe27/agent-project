conversation_history = []

MAX_HISTORY = 10
# summary = ""
# summarize_history()   

def get_messages():

    return conversation_history.copy()


def save_messages(
    messages
):

    global conversation_history

    conversation_history = (
        messages[-MAX_HISTORY:]
    )