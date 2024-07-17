from typing import Tuple
from lol_chatter_backend.DTOs import ErrorDTO, UserLoginDTO, UserSignUpDTO
from lol_chatter_backend.Models.User import User
from sqlalchemy.orm import Session

from lol_chatter_backend.Security.hashing import hash_password, verify_password


def create_user(dp: Session, user: UserSignUpDTO) -> Tuple[User | None, ErrorDTO | None]:
    """
    Creates a new user in the database.

    Parameters:
        dp (Session): The database session to perform the operation.
        user (UserSignUpDTO): The user data to create the new user.

    Returns:
        Tuple[int | None, ErrorDTO | None]: The user ID if creation is successful, else None and an error message.
    """
    if dp.query(User).filter(User.email == user.email).first():
        return  None, ErrorDTO(message="User with that email already exists")

    hashed_pass = hash_password(user.password)
    try:
        db_user = User(
            first_name=user.firstName,
            last_name=user.lastName,
            email=user.email,
            hashed_password=hashed_pass,
        )
        dp.add(db_user)
        dp.commit()
        dp.refresh(db_user)
    except Exception as e:
        print(e)
        return None, ErrorDTO(message="Failed to create user")
    return db_user, None


def login_user(dp: Session, user: UserLoginDTO) -> Tuple[User | None, ErrorDTO | None]:
    """
    Logs in a user.

    Parameters:
        dp (Session): The database session to perform the operation.
        user (UserLoginDTO): The user data to login.

    Returns:
        ErrorDTO | None: An error message if login fails, else None.
    """
    dbUser = dp.query(User).filter(User.email == user.email).first()
    if dbUser is None:
        return  None,ErrorDTO(message="User with that email does not exist")
    if not verify_password( user.password , dbUser.hashed_password):
        return  None,ErrorDTO(message="Wrong password")
    return dbUser, None


def get_user_by_email(dp: Session, email: str) -> Tuple[User | None, ErrorDTO | None]:
    """
    Retrieves a user from the database by email.

    Parameters:
        dp (Session): The database session to perform the operation.
        email (str): The email of the user to retrieve.

    Returns:
        Tuple[User | None, ErrorDTO | None]: The user if found, else None and an error message.
    """
    try:
        user = dp.query(User).filter(User.email == email).first()
    except Exception as e:
        print(e)
        return None, ErrorDTO(message="Failed to get user")
    return user, None
