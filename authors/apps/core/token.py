import jwt
import datetime
from authors.settings import SECRET_KEY


def generate_token(identity: dict, expiry: float = 86400):
    """
    Method that generates a JSON Web Token for the user
    :param identity: User information to be encoded as a dictionary
    :return: JWT token
    :rtype: bytes
    """
    payload = dict(
        identity=identity,
        iat=datetime.datetime.utcnow(),
        exp=datetime.datetime.utcnow() + datetime.timedelta(seconds=expiry))
    return jwt.encode(payload, SECRET_KEY).decode()
