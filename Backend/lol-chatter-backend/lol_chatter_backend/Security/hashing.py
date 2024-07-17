import bcrypt

def hash_password(password : str):
    """
    Hashes a given password using the bcrypt algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.

    Raises:
        None.
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def verify_password(password : str, hashed_password):
    """
    A function to verify a password by checking it against a hashed password.

    Args:
        password (str): The plain text password to be checked.
        hashed_password: The hashed password to be compared with.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False