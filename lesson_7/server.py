import sys
import logging
import logs.server_log_config
from socket import AF_INET, SOCK_STREAM, socket
from common.utils import read_requests, write_responses
from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, PRESENCE, TIME, \
    USER, ACCOUNT_NAME, RESPONSE, ERROR
from select import select

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

    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind((address, port))
        sock.listen(MAX_CONNECTIONS)
        sock.settimeout(1)
        client_sockets = []
        print('Сервер("Общий чат")\n'
              'Кто присылает: Сообщение')
        while True:
            try:
                CLIENT, ADDR = sock.accept()
            except OSError as e:
                pass
            else:
                client_sockets.append(CLIENT)
                SERVER_LOGGER.debug(f'Соединение установлено. Адрес - {ADDR}')

            finally:
                wait = 0
                r_clients = []
                w_clients = []
                try:
                    r_clients, w_clients, _ = select(client_sockets, client_sockets, [], wait)
                except Exception as e:
                    pass

                requests = read_requests(r_clients, client_sockets)
                if requests:
                    SERVER_LOGGER.debug(f'Cообщения от клиентов: {requests}')
                    write_responses(requests, w_clients, client_sockets)
                    SERVER_LOGGER.info(f'Сообщения переданы клиентам.')


if __name__ == '__main__':
    command_line_options()
