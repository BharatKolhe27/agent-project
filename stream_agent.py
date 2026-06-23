import json

from planner import plan
from executor import (
    execute_action,
    TOOLS
)


def stream_agent(
    question,
    max_steps=5
):

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(max_steps):

        yield {
            "type": "status",
            "message": f"Planning Step {step}"
        }

        decision = plan(messages)

        yield {
            "type": "planner",
            "step": step,
            "action": decision.action,
            "args": decision.args
        }

        if decision.action == "final":
            print("final decision")
            print(decision.answer)
            yield {
                "type": "final",
                "answer": decision.answer
            }

            return

        if decision.action not in TOOLS:

            yield {
                "type": "error",
                "message": f"Unknown tool: {decision.action}"
            }

            return

        result = execute_action(
            decision.action,
            decision.args
        )

        yield {
            "type": "tool",
            "tool": decision.action,
            "result": result
        }

        messages.append(
            {
                "role": "assistant",
                "content": str(decision)
            }
        )

        messages.append(
            {
                "role": "tool",
                "content": json.dumps(
                    result,
                    indent=2
                )
            }
        )       

    yield {
        "type": "error",
        "message": "Max steps reached"
    }