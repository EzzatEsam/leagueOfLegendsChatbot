from sqlalchemy import  Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column, Mapped, relationship
from lol_chatter_backend.DbInitialization import Base


class User(Base):
    """
    A class to represent a person.

    ...

    Attributes
    ----------
    id : int
        unique identifier of the user
    first_name : str
        first name of the user
    last_name : str
        last name of the user
    email : str
        email address of the user
    hashed_password : str
        hashed password of the user

    Methods
    -------
    info(additional=""):
        Stub method for future implementations.
    """
    
    __tablename__ = "users"

    id : Mapped[int]  = mapped_column(Integer, primary_key=True, index=True)
    first_name : Mapped[str]  = mapped_column(String(255))
    last_name : Mapped[str]  = mapped_column(String(255))
    email : Mapped[str]  = mapped_column(String(255))
    hashed_password : Mapped[str]  = mapped_column(String(255))
    chat_sessions = relationship(
        "ChatSession", back_populates="user"
    )
