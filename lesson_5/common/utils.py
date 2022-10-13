import json
from .variables import ENCODING, MAX_PACKAGE_LENGTH


def send_msg(sock, msg):
    if not isinstance(msg, dict):
        raise TypeError
    msg_as_str = json.dumps(msg)
    encoded_msg = msg_as_str.encode(ENCODING)
    sock.send(encoded_msg)


def get_msg(sock):
    encoded_msg = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_msg, bytes):
        response_as_str = encoded_msg.decode(ENCODING)
        response = json.loads(response_as_str)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError
