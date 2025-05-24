from logger import InteractionLogger
from database import DatabaseManager
from llm_manager import LLMManager
from sql_generator import SQLQueryGenerator
from response_generator import ResponseGenerator

class SQLChatBot:
    def __init__(self, db_uri: str, model_config: dict):
        self.logger = InteractionLogger()
        self.db_manager = DatabaseManager(db_uri)  
        self.llm_manager = LLMManager(model_config)
        self.sql_generator = SQLQueryGenerator(
            self.llm_manager.get_llm(),
            self.db_manager
        )

        self.response_generator = ResponseGenerator(
            self.llm_manager.get_llm()
        )

    def create_interaction_record(self, question: str, sql: str, result: str, response: str) -> dict:
        
        return {
            "user_question": question,
            "generated_sql": sql,
            "query_result": result,
            "response": response
        }

    def process_question(self, question: str) -> str:
        try:
            
            sql = self.sql_generator.generate_sql(question)

            
            result = self.db_manager.execute_query(sql)

            
            response = self.response_generator.generate_response(question, result)

            
            self.logger.log_interaction(
                self.create_interaction_record(question, sql, result, response)
            )

            return response

        except Exception as e:
            
            error_msg = f"Error processing query: {str(e)}"
            self.logger.log_interaction({
                "user_question": question,
                "error": error_msg
            })

            return error_msg

    def run(self):
        print("Chatbot Initialized. Type 'exit' to quit")

        while True:
            try:
                question = input("\nUser: ")
                if question.lower() in ["exit", "quit"]:
                    break

                response = self.process_question(question)
                print(f"\nAssistant: {response}")

            except KeyboardInterrupt:
                print("\nSession ended.")
                break
