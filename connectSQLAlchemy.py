import tkinter as tk
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
import urllib

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

# Define the SQLAlchemy engine and metadata

metadata = MetaData()

# Define a User class for SQLAlchemy ORM
users_table = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('password', String),
)

metadata.create_all(engine)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Create the Tkinter GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("User Authentication")

        # Create labels and entry widgets
        self.label_username = tk.Label(root, text="Username:")
        self.entry_username = tk.Entry(root)
        self.label_password = tk.Label(root, text="Password:")
        self.entry_password = tk.Entry(root, show="*")

        # Create a login button
        self.button_login = tk.Button(root, text="Login", command=self.login)

        # Pack widgets
        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.button_login.pack()

    def login(self):
        # Retrieve username and password from entry widgets
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check user credentials against the database
        if self.authenticate_user(username, password):
            print("Login successful")
        else:
            print("Login failed")


    def authenticate_user(self, username, password):
        # Establish a connection
        connection = engine.connect()

        try:
            # Query the database for the user with the given credentials
            query = users_table.select().where(
                users_table.c.username == username and users_table.c.password == password)
            result = connection.execute(query)
            user = result.fetchone()

            # Return True if user exists, False otherwise
            return user is not None
        finally:
            # Close the connection
            connection.close()

# Create an instance of the Tkinter application
root = tk.Tk()
app = App(root)

# Run the Tkinter main loop
root.mainloop()
