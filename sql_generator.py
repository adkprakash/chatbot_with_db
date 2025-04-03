from langchain.chains import create_sql_query_chain
from langchain_core.prompts import PromptTemplate
from .database import DatabaseManager

class SQLQueryGenerator:
    
    def __init__(self, llm, db_manager: DatabaseManager):
        self.llm = llm
        self.db_manager = db_manager
        self._init_prompt_template()

    def _init_prompt_template(self):
        self.sql_prompt = PromptTemplate(
            template="""You are a SQL expert. Given the following database schema, write a SQL query to answer the question.
                Follow these rules:
                - Use only the tables and columns listed in the schema
                - Do not include any explanations or markdown formatting
                - Return valid SQL syntax for the database's dialect
                - Use LIMIT {top_k} if needed

                Schema:
                {table_info}

                Question: {input}

                SQL Query:""",
            input_variables=["input", "top_k", "table_info"]
        )

    def generate_sql(self, question: str, top_k: int = 5) -> str:
        schema = self.db_manager.db.get_table_info()
        print(schema)
        
        chain = create_sql_query_chain(
            llm=self.llm,
            db=self.db_manager.db,
            prompt=self.sql_prompt
        )

        result = chain.invoke({
            "input": question,
            "table_info": schema,
            "top_k": top_k
        })
        return result