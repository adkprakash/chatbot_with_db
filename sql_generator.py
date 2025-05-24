from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_core.prompts import PromptTemplate
from database import DatabaseManager
import re
import logging

class SQLQueryGenerator:
    def __init__(self, llm, db_manager: DatabaseManager):
        self.llm = llm
        self.db_manager = db_manager
        self._init_prompt_template()

    def _init_prompt_template(self):
        self.sql_prompt = PromptTemplate(
            template="""You are a SQL expert. Given the following database schema, write a SQL query to answer the question.
                Follow these rules STRICTLY:
                1. Use only the tables/columns in the schema
                2. Return ONLY SQL code with NO explanations
                3. Use SHOW TABLES for listing tables
                4. Never use INFORMATION_SCHEMA
                5. Never include placeholders
                6. Database name is chinook

                Tools: {tools}
                Tool Names: {tool_names}
                
                Schema:
                {schema}

                Question: {input}

                {agent_scratchpad}
                FINAL SQL ANSWER:
                """,
            input_variables=["input", "tools", "tool_names", "schema", "agent_scratchpad"]
        )

    def generate_sql(self, question: str) -> str:
        try:
            schema = self.db_manager.get_table_info()
            toolkit = SQLDatabaseToolkit(db=self.db_manager.db, llm=self.llm)

            agent_executor = create_sql_agent(
                llm=self.llm,
                toolkit=toolkit,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                prompt=self.sql_prompt,
                verbose=False,
                handle_parsing_errors=True,
                max_iterations=3
            )

            response = agent_executor.invoke({
                "input": question,
                "tools": toolkit.get_tools(),
                "tool_names": ", ".join([t.name for t in toolkit.get_tools()]),
                "schema": schema,
                "agent_scratchpad": ""
            })

            # Safe extraction of response
            if isinstance(response, dict):
                output = response.get("output", "")
            else:
                output = str(response)

            # Clean SQL query and check validity
            sql = self._clean_sql(output)

            if not sql.lower().startswith(("select", "show", "insert", "update", "delete")):
                raise ValueError(f"LLM output did not contain valid SQL: {output}")

            return sql

        except Exception as e:
            logging.error(f"Error generating SQL for question '{question}': {str(e)}")
            return "SELECT 'LLM failed to generate valid SQL' AS error_message;"

    def _clean_sql(self, output: str) -> str:
        # Extract SQL from markdown code block
        match = re.search(r"```sql\s*(.*?)```", output, re.DOTALL)
        if match:
            return match.group(1).strip()

        # Fallback to final answer line
        match = re.search(r"FINAL SQL ANSWER:\s*(.*?);", output, re.DOTALL)
        if match:
            return match.group(1).strip() + ";"

        # Try to extract any SQL statement
        match = re.search(r"(SELECT|SHOW|INSERT|UPDATE|DELETE|CREATE|DROP)\s+.*?;", output, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(0).strip()

        return ""