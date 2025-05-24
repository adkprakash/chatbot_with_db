from chatbot import SQLChatBot
from langchain_community.llms import Ollama
from database import DatabaseManager

if __name__ == "__main__":
    db_uri = "mysql+pymysql://root:prakash@localhost:3306/Chinook"
    model_config = {
        "model": "llama3",
        "temperature": 0.2,
        "max_tokens": 2000,
        "n_ctx": 4096,
        "n_gpu_layers": 40,
        "verbose": False
    }

    chatbot = SQLChatBot(db_uri=db_uri, model_config=model_config)  
    chatbot.run()
