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
        """Connect to the database and create the engine."""
        try:
            self.engine = create_engine(
                self.db_uri,
                connect_args={'ssl': False, 'connect_timeout': 10}
            )
            self.db = SQLDatabase(self.engine)
            self._verify_connection()
            print("Connection to the database was successful!")
        except SQLAlchemyError as e:
            logging.error(f"Connection failed: {str(e)}")
            raise RuntimeError(f"Database error: {str(e)}")

    def _verify_connection(self):
        """Test the database connection by executing a simple query."""
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
                
                # Process the result into the requested format
                if result_format == "string":
                    return "\n".join([str(row) for row in result])
                elif result_format == "list":
                    # Convert each row into a dictionary using the column names
                    return [dict(zip(result.keys(), row)) for row in result]
                elif result_format == "json":
                    # Convert each row into a dictionary using the column names
                    return [dict(zip(result.keys(), row)) for row in result]
                else:
                    logging.warning("Unknown result format. Returning as string.")
                    return "\n".join([str(row) for row in result])
        except SQLAlchemyError as e:
            logging.error(f"Query execution failed: {str(e)} - Query: {query}")
            return f"Error: {str(e)}"


    def get_table_info(self) -> str:
        """Return table information."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SHOW TABLES"))
                tables = [row[0] for row in result]
                logging.debug(f"Tables in database: {tables}")
                return tables
        except SQLAlchemyError as e:
            logging.error(f"Failed to get table information: {str(e)}")
            return f"Error fetching table info: {str(e)}"

    def reconnect(self):
        """Attempt to reconnect to the database."""
        logging.info("Attempting to reconnect to the database...")
        try:
            self._connect()
        except RuntimeError as e:
            logging.error(f"Reconnection failed: {str(e)}")


"""if __name__ == "__main__":
    # Database URI for MySQL (replace with your own if needed)
    db_uri = "mysql+pymysql://root:prakash@localhost:3306/Chinook"

    # Create a DatabaseManager instance
    db_manager = DatabaseManager(db_uri)

    # Check table information
    print("Fetching table information:")
    table_info = db_manager.get_table_info()
    print(table_info)

    # Test a query execution
    query = "SELECT * FROM genre LIMIT 5"
    print("\nExecuting query:", query)
    query_result = db_manager.execute_query(query, result_format="list")
    print(query_result)
"""