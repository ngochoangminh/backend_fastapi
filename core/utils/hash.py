import bcrypt
import jwt
import random
import string

def get_random_pwd(length: int):
    """ Create random password
    """
    characters = string.ascii_letters + string.digits
    result = ''.join(random.choice(characters) for i in range(length))
    return result

def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def check_password(password: str, password_hashed):
    if bcrypt.checkpw(password.encode('utf-8'), password_hashed.encode('utf-8')):
        return True
    else:
        return False

def jwt_hash(data: dict, secret_key: str) -> str:
    return jwt.encode(data, secret_key, algorithm="HS256")

def jwt_decode(token: str, secret_key: str) -> dict:
    token = jwt.decode(token, secret_key, algorithms=["HS256"], options={"verify_signature": False})
    return token