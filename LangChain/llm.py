from langchain_openai import ChatOpenAI


def get_llm():
    return ChatOpenAI(
        base_url="http://127.0.0.1:1234/v1",
        api_key="lm-studio",
        model="qwen3.5-2b",
        temperature=0.2,
    )