from azure.identity import DefaultAzureCredential
import pyodbc

import os
os.environ["AZURE_SUBSCRIPTION_ID"] = "deb58934-a5b1-41b2-b7e6-d87c359af07d"
os.environ["AZURE_TENANT_ID"] = "8acbc2c5-c8ed-42c7-8169-ba438a0dbe2f"
os.environ["AZURE_CLIENT_ID"] = "bba51d91-1ffe-48ba-9704-9569246ee081"
os.environ["AZURE_CLIENT_SECRET"] = "oSfJu980jd"



# Use the default managed identity credential
credential = DefaultAzureCredential()

# Set up the connection string with the Azure SQL Database details
server_name = "wms-uni.database.windows.net"
database_name = "WMS_UNI"

# Construct the connection string

connection_string = (
    f"Driver={{SQL Server Native Client 11.0}};"
    f"Server=tcp:{server_name},1433;"
    f"Database={database_name};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)


# Create a connection using pyodbc and the managed identity credential
with pyodbc.connect(connection_string, attrs_before={0: b"Set_AZURE_AD_INTERACTIVE=true"}, autocommit=True, timeout=10) as conn:
    # Now you can use 'conn' to interact with the Azure SQL Database
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
