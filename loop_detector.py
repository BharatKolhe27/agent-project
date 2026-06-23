def detect_loop(trace):

    if len(trace) < 3:
        return False

    last = [
        x["tool"]
        for x in trace[-3:]
    ]

    return len(set(last)) == 1