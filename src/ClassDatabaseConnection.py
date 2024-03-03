import os
import urllib
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pyodbc
import time

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
        conStr = f'Driver={driver};Server=tcp:{server},1433;Database={database}' \
                 f';Uid={user};Pwd={password}' \
                 f';Encrypt=yes;TrustServerCertificate=no; Connect Timeout=5;'

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

    def test_connectivity(self, max_attempts=3, delay_between_attempts=1):
        for attempt in range(max_attempts):
            try:
                # Attempt to create a connection without opening it
                conn = self.engine.raw_connection()
                conn.close()
                return 'Connection Established'
            except pyodbc.Error as e:
                # Handle specific pyodbc errors
                error_code = e.args[0]
                if error_code == '08001':
                    return 'Failed to connect: Server not found or inaccessible'
                elif error_code == '28000':
                    return 'Failed to connect: Authentication failed'
                else:
                    if attempt < max_attempts - 1:
                        time.sleep(delay_between_attempts)
                        continue
                    else:
                        return f'Failed to connect after {max_attempts} attempts: {str(e)}'
            except Exception as e:
                # Handle other exceptions
                if attempt < max_attempts - 1:
                    time.sleep(delay_between_attempts)
                    continue
                else:
                    return f"Failed to connect after {max_attempts} attempts: {str(e)}"



# #Usage:
# db = DatabaseConnection()
# session = db.get_session()





