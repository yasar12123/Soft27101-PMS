
from src.ClassUser import User  # Import your User class

from sqlalchemy.orm import sessionmaker
from src.ClassDatabaseConnection import DatabaseConnection



 # Create a sessionmaker bound to the engine
db = DatabaseConnection()
engine = db.get_engine()
session = sessionmaker(bind=engine)

session = session()
# Query the database for the user with the given username
username = 'tst'
passw = '12345'

user = User()
#user = session.query(User).filter_by(username=username).first()


a = user.authenticate(username, passw)

print(a)