from dbConnection import dbInitalise
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the SQLAlchemy engine and metadata
engine, metadata = dbInitalise()



class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    #user_name: Mapped[str]
    #type: Mapped[str]

    #def __repr__(self):
      #  return f"{self.__class__.__name__}({self.name!r})"


# create a session to manage the connection to the database
Session = sessionmaker(bind=engine)
session = Session()
users = session.query(User).all()
print(users)