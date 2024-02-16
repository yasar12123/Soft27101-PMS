import os
import urllib
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

class DatabaseConnection:
    def __init__(self):
        load_dotenv()
        conn_str = self.connection_string()
        self.engine = create_engine(conn_str, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def connection_string(self):
        server = os.getenv('AZURE_SQL_SERVER')
        database = os.getenv('AZURE_SQL_DB')
        driver = '{ODBC Driver 18 for SQL Server}' ##pc with driver
        #driver = '{SQL Server Native Client 11.0}' ##laptop with ssms
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
            print(f"Error executing query: {e}")

    def get_session(self):
        return self.Session





#Usage:
# db = DatabaseConnection()
# session = db.get_session()





