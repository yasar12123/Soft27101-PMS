import os

import pandas as pd
from sqlalchemy import create_engine

server = 'wms-uni.database.windows.net'
database = 'WMS_UNI'
driver= '{ODBC Driver 18 for SQL Server}'

username = os.getenv('wms_admin')
password = os.getenv('AZURE!log')

odbc_params = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'

connection_string = f'mssql+pyodbc:///?odbc_connect={odbc_params}'

engine = create_engine(connection_string)

# query sys.databases view

query = '''
        SELECT
               [name]
              ,[database_id]
       FROM [sys].[databases];
'''

df = pd.read_sql(query, engine)
print(df.head())

engine.dispose()