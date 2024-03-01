import os
import urllib
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pyodbc

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
        driver = os.getenv('SQL_DRIVER', '{ODBC Driver 17 for SQL Server}')  ## test older version
        #driver = os.getenv('SQL_DRIVER', '{ODBC Driver 18 for SQL Server}') ##pc with driver
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
        try:
            return self.Session
        except pyodbc.OperationalError as e:
            return RuntimeError("Error establishing connection: {}".format(str(e)))

    def test_connectivity(self):
        try:
            # Attempt to create a connection without opening it
            conn = self.engine.raw_connection()
            conn.close()
            return 'Connection Established'
        except Exception as e:
            # Raise a RuntimeError if an exception occurs
            raise RuntimeError(f"Failed to connect to the server: {str(e)}")



# #Usage:
# db = DatabaseConnection()
# session = db.get_session()





