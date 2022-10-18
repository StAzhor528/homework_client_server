import json
import os
import sys
import logging

sys.path.append(os.path.join(os.getcwd(), '..'))
from .variables import ENCODING, MAX_PACKAGE_LENGTH
from functools import wraps
import traceback


def log(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        script_name = sys.argv[0].split('/')[-1]

        if script_name == 'client.py':
            FUNC_LOGGER = logging.getLogger('client')
        elif script_name == 'server.py':
            FUNC_LOGGER = logging.getLogger('server')
        f = func(*args, **kwargs)
        main_func = traceback.format_stack()
        FUNC_LOGGER.info(f'Вызванна функция {func.__name__} c аргументами {args}, {kwargs}')
        FUNC_LOGGER.info(
            f'Функция {func.__name__} вызвана из функции {traceback.format_stack()[0].strip().split()[-1]}')
        return f

    return wrap


@log
def send_msg(sock, msg):
    if not isinstance(msg, dict):
        raise TypeError
    msg_as_str = json.dumps(msg)
    encoded_msg = msg_as_str.encode(ENCODING)
    sock.send(encoded_msg)


@log
def get_msg(sock):
    encoded_msg = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_msg, bytes):
        response_as_str = encoded_msg.decode(ENCODING)
        response = json.loads(response_as_str)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError
