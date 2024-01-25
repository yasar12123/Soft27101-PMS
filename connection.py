import urllib
from sqlalchemy import create_engine, text


server = 'wms-uni.database.windows.net'
database = 'WMS_UNI'
#driver = '{ODBC Driver 18 for SQL Server}'
driver = '{SQL Server Native Client 11.0}'
user = 'wms_admin'
password = 'AZURE!log'



conn = f"""Driver={driver};Server=tcp:{server},1433;Database={database};
Uid={user};Pwd={password};Encrypt=yes;TrustServerCertificate=no;"""

params = urllib.parse.quote_plus(conn)
conn_str = 'mssql+pyodbc:///?autocommit=true&odbc_connect={}'.format(params)
engine = create_engine(conn_str, echo=True)



stmt = text("SELECT * FROM WMS_UNI.DBO.FACT_TEST")
with engine.connect() as conn:
    result = conn.execute(stmt)

