from langchain_community.utilities import SQLDatabase

class DatabaseManager:
    def __init__(self):
        self.user:"localhost"
        self.password:""
        self.port:3360
        self.host:"root"
        self.database:"Chinook"
        
    
    def __init__(self):
        db_uri=f"mysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        

        def execute_query(self, query: str)-> str: 
            return self.db.run(query)

        def get_schema(self) -> str:
            return self.db.get_table_info()
