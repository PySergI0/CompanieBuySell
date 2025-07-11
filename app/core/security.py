from passlib.context import CryptContext
from passlib.exc import UnknownHashError

# Настройка контекста хеширования
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_password_hash(password: str) -> str:
    """
    Generates a hash of the password.
    
    Args:
        password: The password is in its purest form
        
    Returns:
        The hashed password
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if the password matches its hash.
    
    Args:
        plain_password: The password is in its purest form
        hashed_password: The hashed password from the DB
        
    Returns:
        bool: True if the password is correct, False if not
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        return False