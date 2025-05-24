from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence


class ResponseGenerator:
    def __init__(self, llm):
        """
        Initializes the response generator with an LLM and a custom chatbot prompt template.
        """
        self.llm = llm
        self._init_response_template()

    def _init_response_template(self):
        """
        Sets up the prompt template for generating chatbot responses.
        """
        self.response_prompt = PromptTemplate(
            template="""
You're a smart, friendly chatbot helping users understand information from a database.

Use the query result below to answer the user's question naturally. Be accurate, concise, and avoid adding made-up data. 
If the result is empty or unclear, let the user know gently.

Stay conversational — you're talking to a human.

Question: {question}
Query Result: {result}

Chatbot:
""",
            input_variables=["question", "result"]
        )

        # Create a chain using the new preferred syntax
        self.chain: RunnableSequence = self.response_prompt | self.llm

    from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence


class ResponseGenerator:
    def __init__(self, llm):

        self.llm = llm
        self._init_response_template()

    def _init_response_template(self):

        self.response_prompt = PromptTemplate(
            template="""
                You're a smart, friendly chatbot helping users understand information from a database.

                Use the query result below to answer the user's question naturally. Be accurate, concise, and avoid adding made-up data. 
                If the result is empty or unclear, let the user know gently.

                Stay conversational — you're talking to a human.

                Question: {question}
                Query Result: {result}

                Chatbot:
                """,
            input_variables=["question", "result"]
        )

        
        self.chain: RunnableSequence = self.response_prompt | self.llm

    def generate_response(self, question: str, result: str) -> str:

        output = self.chain.invoke({
            "question": question,
            "result": result
        })

        
        if isinstance(output, str):
            return output.strip()
        elif isinstance(output, dict) and "text" in output:
            return output["text"].strip()
        else:
            return str(output).strip()

        output = self.chain.invoke({
            "question": question,
            "result": result
        })

        
        if isinstance(output, str):
            return output.strip()
        elif isinstance(output, dict) and "text" in output:
            return output["text"].strip()
        else:
            return str(output).strip()
