import json


def send_msg(sock, msg, encoding='utf-8'):
    msg_as_str = json.dumps(msg)
    encoded_msg = msg_as_str.encode(encoding)
    sock.send(encoded_msg)


def get_msg(sock, encoding='utf-8'):
    encoded_msg = sock.recv(4096)
    if isinstance(encoded_msg, bytes):
        response_as_str = encoded_msg.decode(encoding)
        response = json.loads(response_as_str)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


