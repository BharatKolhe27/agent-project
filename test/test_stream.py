from stream_agent import stream_agent

for event in stream_agent(
    "What's the weather in Indore and save it as a note"
):
    print(event)