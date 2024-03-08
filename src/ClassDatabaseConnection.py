import os
import urllib
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pyodbc
import time


class DatabaseConnection:
    """
    Class to handle database connection and session queries
    Attributes:
        engine: sqlalchemy engine object
        Session: sqlalchemy session object
    Methods:
        connection_string(): returns the connection string for the database
        create_engine(): creates a sqlalchemy engine object
        test_connectivity(max_attempts=3, delay_between_attempts=1): tests the connection to the database
        execute_query(query, params=None): executes a query on the database
        get_session(): returns a sqlalchemy session object
    """
    def __init__(self):
        """
        Initializes the DatabaseConnection class
        """
        load_dotenv()
        self.engine = self.create_engine()
        self.Session = sessionmaker(bind=self.engine)

    def connection_string(self):
        """
        Returns the connection string for the database
        requirements: AZURE_SQL_SERVER, AZURE_SQL_DB, AZURE_SQL_USER, AZURE_SQL_PASS
        :return: str
        """
        server = os.getenv('AZURE_SQL_SERVER')
        database = os.getenv('AZURE_SQL_DB')
        #driver = os.getenv('SQL_DRIVER', '{ODBC Driver 17 for SQL Server}')  ## test older version
        driver = os.getenv('SQL_DRIVER', '{ODBC Driver 18 for SQL Server}') ##pc with driver
        #driver = os.getenv('SQL_DRIVER', '{SQL Server Native Client 11.0}') ##laptop with ssms

        user = os.getenv('AZURE_SQL_USER')
        password = os.getenv('AZURE_SQL_PASS')
        conStr = f'Driver={driver};Server=tcp:{server},1433;Database={database}' \
                 f';Uid={user};Pwd={password}' \
                 f';Encrypt=yes;TrustServerCertificate=no; Connect Timeout=30;'

        params = urllib.parse.quote_plus(conStr)
        return 'mssql+pyodbc:///?autocommit=true&odbc_connect={}'.format(params)

    def create_engine(self):
        """
        Creates a sqlalchemy engine object
        :return: sqlalchemy engine object
        """
        conn_str = self.connection_string()
        return create_engine(conn_str, echo=False)

    def test_connectivity(self, max_attempts=3, delay_between_attempts=1):
        """
        Tests the connection to the database
        :param max_attempts: int, maximum number of attempts to connect to the database
        :type max_attempts: int
        :param delay_between_attempts: int, number of seconds to wait between attempts
        :type delay_between_attempts: int
        :return: str, success message or error message
        """
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

    def execute_query(self, query, params=None):
        """ Executes a query on the database
        :param query: str, query to execute
        :type query: str
        :param params: dict, parameters to pass to the query
        :type params: dict
        :return: list, list of query results
        """

        try:
            with self.engine.connect() as connection:
                if isinstance(query, str):
                    query = text(query)
                result = connection.execute(query, params)
                return result.fetchall()
        except Exception as e:
            raise RuntimeError(f"Error executing query: {e}")

    def get_session(self):
        """ Returns a sqlalchemy session object
        :return: sqlalchemy session object
        """
        try:
            return self.Session
        except pyodbc.OperationalError as e:
            return RuntimeError("Error establishing connection: {}".format(str(e)))





# #Usage:
# db = DatabaseConnection()
# session = db.get_session()





