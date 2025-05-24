from langchain_ollama import OllamaLLM

class LLMManager:
    

    def __init__(self, model_config: dict):
        self.llm= OllamaLLM(**model_config)

    def get_llm(self):
        return self.llm