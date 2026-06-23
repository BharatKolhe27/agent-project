import json
import time

from planner import plan
from loop_detector import (
    detect_loop
)

from metrics import Metrics
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
    metrics = Metrics()
    messages = get_messages()

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    trace = []

    for step in range(max_steps):

        metrics.add_llm_call()
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
                    trace,

                "metrics":
                    metrics.to_dict()
            }
        if decision.action not in TOOLS:

          return {
                "answer":
                    decision.answer,

                "trace":
                    trace,

                "metrics":
                    metrics.to_dict()
            }

        if not validate_action(
            decision.action,
            decision.args
        ):

            return {
                "answer":
                    decision.answer,

                "trace":
                    trace,

                "metrics":
                    metrics.to_dict()
            }

        start = time.time()

        metrics.add_tool_call()
        
        result = execute_action(
            decision.action,
            decision.args
        )

        latency = (
            time.time() - start
        )
        metrics.add_latency(
                        latency
                    )
        trace.append(
        {
            "step": step,
            "reasoning": decision.reasoning,
            "tool": decision.action,
            "args": decision.args,
            "result": result
        }
    )
        
        if detect_loop(trace):

            return {
                "answer":
                    decision.answer,

                "trace":
                    trace,

                "metrics":
                    metrics.to_dict()
            }

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
            decision.answer,

        "trace":
            trace,

        "metrics":
             metrics.to_dict()
        }