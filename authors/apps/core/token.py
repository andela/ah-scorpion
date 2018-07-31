import jwt
import datetime
from authors.settings import SECRET_KEY


def generate_token(identity: dict):
    """
    Method that generates a JSON Web Token for the user
    :param identity: User information to be encoded as a dictionary
    :return: JWT token
    :rtype: bytes
    """
    payload = dict(
        identity=identity,
        iat=datetime.datetime.utcnow(),
        exp=datetime.datetime.utcnow() + datetime.timedelta(days=1))
    return jwt.encode(payload, SECRET_KEY).decode()