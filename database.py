from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

class DatabaseManager:
    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        self.engine = None
        self.db = None
        self._connect()
    

    def _connect(self):
        
        try:
            self.engine = create_engine(
                self.db_uri,
                connect_args={'ssl': False, 'connect_timeout': 10}
            )
            self.db = SQLDatabase(self.engine)
            self._verify_connection()
        except SQLAlchemyError as e:
            logging.error(f"Connection failed: {str(e)}")
            raise RuntimeError(f"Database error: {str(e)}")

    def _verify_connection(self):
      
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logging.debug("Connection test successful.")
        except SQLAlchemyError as e:
            logging.error(f"Connection verification failed: {str(e)}")
            raise RuntimeError(f"Connection verification failed: {str(e)}")

    def execute_query(self, query: str, result_format="string"):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                
                if result_format == "string":
                    return "\n".join([str(row) for row in result])
                elif result_format in ["list", "json"]:
                    return [dict(row) for row in result.mappings()]
                else:
                    logging.warning("Unknown result format. Returning as string.")
                    return "\n".join([str(row) for row in result])
        except SQLAlchemyError as e:
            logging.error(f"Query execution failed: {str(e)}")
            return f"Error: {str(e)}"


    def get_table_info(self) -> str:
      
        try:
            table_info = self.db.get_table_info()
            logging.debug("Fetched table information successfully.")
            return table_info
        except SQLAlchemyError as e:
            logging.error(f"Failed to get table information: {str(e)}")
            return f"Error fetching table info: {str(e)}"

    def reconnect(self):
        
        logging.info("Attempting to reconnect to the database...")
        self._connect()

