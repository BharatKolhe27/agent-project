def validate_action(
    action,
    args
):

    if action == "get_weather":

        city = args.get("city")

        return (
            isinstance(city, str)
            and city.strip()
        )

    if action == "save_memory":

        return (
            isinstance(
                args.get("key"),
                str
            )
            and
            isinstance(
                args.get("value"),
                str
            )
        )

    if action == "get_memory":

        return (
            isinstance(
                args.get("key"),
                str
            )
        )

    if action == "create_note":

        return (
            isinstance(
                args.get("text"),
                str
            )
        )

    return True