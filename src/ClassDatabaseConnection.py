import os
import urllib
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import text


class DatabaseConnection:
    def __init__(self):
        load_dotenv()
        server = os.getenv('AZURE_SQL_SERVER')
        database = os.getenv('AZURE_SQL_DB')
        #driver = '{ODBC Driver 18 for SQL Server}' ##pc with driver
        driver = '{SQL Server Native Client 11.0}' ##laptop with ssms
        user = os.getenv('AZURE_SQL_USER')
        password = os.getenv('AZURE_SQL_PASS')

        conn = f'Driver={driver};Server=tcp:{server},1433;Database={database};Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=no;'
        params = urllib.parse.quote_plus(conn)
        conn_str = 'mssql+pyodbc:///?autocommit=true&odbc_connect={}'.format(params)

        self.engine = create_engine(conn_str, echo=True)
        self.metadata = MetaData()
        self.session = sessionmaker(bind=self.engine)

    def execute_query(self, query, params=None):
        try:
            # Establish a connection
            with self.engine.connect() as connection:
                # If the query is a string, create a text object
                if isinstance(query, str):
                    query = text(query)

                # Execute the query with parameters
                result = connection.execute(query, params)
                return result.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")

    def get_engine(self):
        return self.engine

    def get_metadata(self):
        return self.metadata

    def get_session(self):
        return self.session




#Usage:
# db = DatabaseConnection()
# engine = db.get_engine()
# metadata = db.get_metadata()
# session = db.get_session()
##session()
# #engine.connect()



