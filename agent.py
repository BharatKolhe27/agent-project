import json
import time

from planner import plan

from executor import (
    execute_action,
    TOOLS
)

from validator import (
    validate_action
)

from history import (
    get_messages,
    save_messages
)


def run_agent(
    question,
    max_steps=5
):

    messages = get_messages()

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    trace = []

    for step in range(max_steps):

        decision = plan(
            messages
        )

        print(
            f"\nSTEP {step}"
        )

        print(decision)

        if decision.action == "final":

            messages.append(
                {
                    "role":
                        "assistant",
                    "content":
                        decision.answer
                }
            )

            save_messages(
                messages
            )

            return {
                "answer":
                    decision.answer,
                "trace":
                    trace
            }

        if decision.action not in TOOLS:

            return {
                "answer":
                    "Unknown tool",
                "trace":
                    trace
            }

        if not validate_action(
            decision.action,
            decision.args
        ):

            return {
                "answer":
                    "Validation failed",
                "trace":
                    trace
            }

        start = time.time()

        result = execute_action(
            decision.action,
            decision.args
        )

        latency = (
            time.time() - start
        )

        trace.append(
            {
                "step": step,
                "reasoning":
                    decision.reasoning,
                "tool":
                    decision.action,
                "args":
                    decision.args,
                "result":
                    result,
                "latency":
                    round(
                        latency,
                        3
                    )
            }
        )

        messages.append(
            {
                "role":
                    "assistant",
                "content":
                    str(decision)
            }
        )

        messages.append(
            {
                "role":
                    "tool",
                "content":
                    json.dumps(
                        result,
                        indent=2
                    )
            }
        )

    return {
        "answer":
            "Max steps reached",
        "trace":
            trace
    }