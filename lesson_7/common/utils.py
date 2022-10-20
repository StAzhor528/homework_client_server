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
        FUNC_LOGGER.info(f'Вызванна функция {func.__name__} c аргументами {args}, {kwargs}')
        FUNC_LOGGER.info(
            f'Функция {func.__name__} вызвана из функции {traceback.format_stack()[0].strip().split()[-1]}')
        return f

    return wrap


@log
def write_responses(requests, w_clients, all_clients):
    for client_socket in w_clients:
        for sock in requests:
            response = f'{sock.fileno()}: {requests[sock]}'
            try:

                client_socket.send(response.encode(ENCODING))
            except Exception:
                print(f'Клиент {client_socket.fileno()} отключился')
                all_clients.remove(client_socket)
                client_socket.close()
    print(response)


@log
def read_requests(r_clients, all_clients):
    responses = {}
    for client_socket in r_clients:
        try:
            encoded_msg = client_socket.recv(MAX_PACKAGE_LENGTH).decode(ENCODING)
            responses[client_socket] = encoded_msg
        except Exception:
            print(f'Клиент {client_socket.fileno()} отключился')
            all_clients.remove(client_socket)
    return responses
