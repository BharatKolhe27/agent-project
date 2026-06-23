# test_plan.py

from planner import plan

messages = [
    {
        "role": "user",
        "content":
        "Remember my favorite language is Spanish"
    }
]

decision = plan(
    messages
)

print(decision)
print(type(decision))