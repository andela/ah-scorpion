import jwt
import datetime
from authors.settings import SECRET_KEY


<<<<<<< HEAD
def generate_token(identity: dict, expiry: float = 86400):
=======
def generate_token(identity: dict):
>>>>>>> 6252091f7c17e7ffa9e1d9fb87ce196f3c34001d
    """
    Method that generates a JSON Web Token for the user
    :param identity: User information to be encoded as a dictionary
    :return: JWT token
    :rtype: bytes
    """
    payload = dict(
        identity=identity,
        iat=datetime.datetime.utcnow(),
<<<<<<< HEAD
        exp=datetime.datetime.utcnow() + datetime.timedelta(seconds=expiry))
=======
        exp=datetime.datetime.utcnow() + datetime.timedelta(days=1))
>>>>>>> 6252091f7c17e7ffa9e1d9fb87ce196f3c34001d
    return jwt.encode(payload, SECRET_KEY).decode()