from langchain_core.runnables import RunnableLambda

def print_tokens(chain_name):
    def _print(message):
        usage = message.usage_metadata or {}

        print(
            f"[{chain_name}] "
            f"Input: {usage.get('input_tokens', 0)} | "
            f"Output: {usage.get('output_tokens', 0)} | "
            f"Total: {usage.get('total_tokens', 0)}"
        )

        return message

    return _print