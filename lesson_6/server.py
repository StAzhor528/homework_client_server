import json
import sys
import logging
import logs.server_log_config
from socket import AF_INET, SOCK_STREAM, socket
from common.utils import get_msg, send_msg
from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, PRESENCE, TIME, \
    USER, ACCOUNT_NAME, RESPONSE, ERROR

SERVER_LOGGER = logging.getLogger('server')


def process_client_message(msg):
    SERVER_LOGGER.info(f'Формирование ответа клиенту.')
    if ACTION in msg and msg[ACTION] == PRESENCE and TIME in msg and USER in msg \
            and msg[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {RESPONSE: 400,
            ERROR: 'Bad Request'}


def command_line_options():
    try:
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port = DEFAULT_PORT
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.error("При запуске сервера после параметра '-p' не указан номер порта.")
        sys.exit()
    except ValueError:
        SERVER_LOGGER.error('При запуске сервера неверно указан номер порта.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            address = sys.argv[sys.argv.index('-a') + 1]
        else:
            address = ''
    except IndexError:
        SERVER_LOGGER.error("При запуске сервера после параметра '-a' не указан адрес.")
        sys.exit(1)
    SERVER_LOGGER.info(f'Сервер запущен.'
                       f'Порт для подключений: {port}'
                       f'Адрес с которого принимаются подключения: {address}'
                       f'Если адрес отсутствует, то соединения возможны с любых адресов.')
    SOCKET = socket(AF_INET, SOCK_STREAM)
    SOCKET.bind((address, port))
    SOCKET.listen(MAX_CONNECTIONS)

    while True:
        CLIENT, ADDR = SOCKET.accept()
        SERVER_LOGGER.debug(f'Соединение установлено. Адрес - {ADDR}')
        try:
            msg_from_client = get_msg(CLIENT)
            SERVER_LOGGER.debug(f'Получено сообщение: {msg_from_client}')
            response = process_client_message(msg_from_client)
            SERVER_LOGGER.info(f'Сформирован следующий ответ клиенту: {response}')
            send_msg(CLIENT, response)
            SERVER_LOGGER.info(f'Сообщение передано клиенту.')
            SERVER_LOGGER.info(f'Соединение с клиентом {ADDR} закрывается.')
            CLIENT.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать json строку, полученную от клиента {ADDR}.')
            SERVER_LOGGER.info(f'Соединение с клиентом {ADDR} закрывается.')
            CLIENT.close()
        except ValueError:
            SERVER_LOGGER.error(f'Приняты некорректные данные от клиента {ADDR}.')
            SERVER_LOGGER.info(f'Соединение с клиентом {ADDR} закрывается.')
            CLIENT.close()


if __name__ == '__main__':
    command_line_options()
