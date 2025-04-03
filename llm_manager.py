from langchain_ollama import OllamaLLM

class LLMManager:
    #LLM configuration and initialization using OllamaLLM

    def __init__(self, model_config: dict):
        self.llm= OllamaLLM(**model_config)

    def get_llm(self):
        return self.llm