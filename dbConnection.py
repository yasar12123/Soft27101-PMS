import os
from sqlalchemy import create_engine, MetaData
import urllib
from dotenv import load_dotenv

load_dotenv()

def dbInitalise():
    # Get env variable
    server = os.getenv('AZURE_SQL_SERVER')
    database = os.getenv('AZURE_SQL_DB')
    driver = '{ODBC Driver 18 for SQL Server}'
    #driver = '{SQL Server Native Client 11.0}'
    user = os.getenv('AZURE_SQL_USER')
    password = os.getenv('AZURE_SQL_PASS')

    # Form connection
    conn = f'Driver={driver};Server=tcp:{server},1433;Database={database};Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=no;'
    params = urllib.parse.quote_plus(conn)
    conn_str = 'mssql+pyodbc:///?autocommit=true&odbc_connect={}'.format(params)

    # Define the SQLAlchemy engine and metadata
    engine = create_engine(conn_str, echo=True)
    metadata = MetaData()

    return engine, metadata
