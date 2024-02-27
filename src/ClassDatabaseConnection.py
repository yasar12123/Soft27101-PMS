import os
import urllib
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

class DatabaseConnection:
    def __init__(self):
        load_dotenv()
        self.engine = self.create_engine()
        self.Session = sessionmaker(bind=self.engine)

    def create_engine(self):
        conn_str = self.connection_string()
        return create_engine(conn_str, echo=False)

    def connection_string(self):
        server = os.getenv('AZURE_SQL_SERVER')
        database = os.getenv('AZURE_SQL_DB')
        #driver = os.getenv('SQL_DRIVER', '{ODBC Driver 17 for SQL Server}')  ## test older version
        driver = os.getenv('SQL_DRIVER', '{ODBC Driver 18 for SQL Server}') ##pc with driver
        #driver = os.getenv('SQL_DRIVER', '{SQL Server Native Client 11.0}') ##laptop with ssms

        user = os.getenv('AZURE_SQL_USER')
        password = os.getenv('AZURE_SQL_PASS')
        conStr = f'Driver={driver};Server=tcp:{server},1433;Database={database};Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=no;'
        params = urllib.parse.quote_plus(conStr)
        return 'mssql+pyodbc:///?autocommit=true&odbc_connect={}'.format(params)

    def execute_query(self, query, params=None):
        try:
            with self.engine.connect() as connection:
                if isinstance(query, str):
                    query = text(query)
                result = connection.execute(query, params)
                return result.fetchall()
        except Exception as e:
            raise RuntimeError(f"Error executing query: {e}")

    def get_session(self):
        return self.Session

    def __enter__(self):
        return self.get_session()

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     if exc_type is not None:
    #         print(f"An error occurred: {exc_val}")
    #     self.Session.close()




# #Usage:
# db = DatabaseConnection()
# session = db.get_session()





