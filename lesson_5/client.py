import json
import sys
import logging
import logs.client_log_config
from socket import AF_INET, SOCK_STREAM, socket
from common.utils import send_msg, get_msg
from datetime import datetime
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, PRESENCE, ACTION, \
    ACCOUNT_NAME, TIME, USER, RESPONSE, STATUS

CLIENT_LOGGER = logging.getLogger('client')


def create_presence(account_name='Guest'):
    CLIENT_LOGGER.info(f'Формирование сообщения-присутствия серверу.')
    msg = {ACTION: PRESENCE,
           TIME: str(datetime.now()),
           USER: {ACCOUNT_NAME: account_name,
                  STATUS: "Привет, я тут!"
                  }
           }
    return msg


def create_answer(msg):
    CLIENT_LOGGER.info(f'Формирование сообщения после полученного ответа от сервера.')
    if RESPONSE in msg:
        if msg[RESPONSE] == 200:
            return 'Все прошло без ошибок!'
        return 'Ошибка!'
    raise ValueError


def command_line_options():
    try:
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port = DEFAULT_PORT
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        CLIENT_LOGGER.error("При запуске клиента после параметра '-p' не указан номер порта.")
        sys.exit()
    except ValueError:
        CLIENT_LOGGER.error('При запуске клиента неверно указан номер порта.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            address = sys.argv[sys.argv.index('-a') + 1]
        else:
            address = DEFAULT_IP_ADDRESS
    except IndexError:
        CLIENT_LOGGER.error("При запуске клиента после параметра '-a' не указан адрес.")
        sys.exit(1)
    CLIENT_LOGGER.info(f'Попытка подсоединения к серверу со стороны клиента.'
                       f'Порт для подключений: {port}'
                       f'Адрес подключения: {address}')
    SOCKET = socket(AF_INET, SOCK_STREAM)
    SOCKET.connect((address, port))
    msg = create_presence()
    send_msg(SOCKET, msg)

    try:
        answer = create_answer(get_msg(SOCKET))
        CLIENT_LOGGER.info(f'Итог: {answer}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error(f'Не удалось декодировать сообщение, полученное от сервера.')
    except ValueError:
        CLIENT_LOGGER.error(f'Приняты некорректные данные от сервера.')
    CLIENT_LOGGER.info(f'Соединение с сервером закрывается.')
    SOCKET.close()


if __name__ == '__main__':
    command_line_options()
