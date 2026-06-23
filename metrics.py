class Metrics:

    def __init__(self):

        self.llm_calls = 0

        self.tool_calls = 0

        self.total_latency = 0

    def add_llm_call(self):

        self.llm_calls += 1

    def add_tool_call(self):

        self.tool_calls += 1

    def add_latency(
        self,
        latency
    ):

        self.total_latency += latency

    def to_dict(self):

        return {
            "llm_calls":
                self.llm_calls,

            "tool_calls":
                self.tool_calls,

            "total_latency":
                round(
                    self.total_latency,
                    3
                )
        }