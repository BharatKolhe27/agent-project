def detect_loop(trace):

    if len(trace) < 3:
        return False

    last_three = trace[-3:]

    same_tool = (
        len(
            set(
                x["tool"]
                for x in last_three
            )
        ) == 1
    )

    same_args = (
        len(
            set(
                str(x["args"])
                for x in last_three
            )
        ) == 1
    )

    return (
        same_tool
        and
        same_args
    )