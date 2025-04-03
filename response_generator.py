from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

class ResponseGenerator:
    def __init__(self,llm):
        self.llm=llm
        self._init_response_template()

    def _init_response_template(self):
        self.response_prompt=PromptTemplate(
            template= "",
            input_variables=["question","result"]
        )
        self.chain=LLMChain(llm=self.llm, prompt=self.response_prompt)

    def generate_response(self, question:str, result:str)->str:
        return self.chain.invoke({
            "question": question,
            "result": result
        })['text']