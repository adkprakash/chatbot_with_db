from .chatbot import SQLChatBot
from langchain_community.llms import Ollama

if __name__ == "__main__":
    model_config = {
        "model": "llama3",
        "temperature": 0.2,
        "max_tokens": 2000,
        "n_ctx": 4096,
        "n_gpu_layers": 40,
        "verbose": False
    }

    chatbot = SQLChatBot(
        db_uri=f"sqlite:///{database}",
        model_config=model_config
    )
    chatbot.run()