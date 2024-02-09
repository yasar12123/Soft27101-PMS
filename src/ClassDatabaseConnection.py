import os
import urllib
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv

class DatabaseConnection:
    def __init__(self):
        load_dotenv()
        server = os.getenv('AZURE_SQL_SERVER')
        database = os.getenv('AZURE_SQL_DB')
        driver = '{ODBC Driver 18 for SQL Server}' ##pc with driver
        # driver = '{SQL Server Native Client 11.0}' ##laptop with ssms
        user = os.getenv('AZURE_SQL_USER')
        password = os.getenv('AZURE_SQL_PASS')

        conn = f'Driver={driver};Server=tcp:{server},1433;Database={database};Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=no;'
        params = urllib.parse.quote_plus(conn)
        conn_str = 'mssql+pyodbc:///?autocommit=true&odbc_connect={}'.format(params)

        self.engine = create_engine(conn_str, echo=True)
        self.metadata = MetaData()

    def get_engine(self):
        return self.engine

    def get_metadata(self):
        return self.metadata

# Usage:
#db = DatabaseConnection()
# engine = db.get_engine()
# metadata = db.get_metadata()



