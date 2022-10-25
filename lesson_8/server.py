import sys
import socket
import logging
import select
import logs.config_server_log
from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, TIME, \
    USER, ACCOUNT_NAME, FROM, PRESENCE, ERROR, MESSAGE, \
    MESSAGE_TEXT, RESPONSE_400, TO, RESPONSE_200, EXIT
from common.utils import get_msg, send_msg, log

SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client, clients, names):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and \
            TIME in message and USER in message:
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_msg(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            send_msg(client, response)
            clients.remove(client)
            client.close()
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TO in message and TIME in message \
            and FROM in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен.'
        send_msg(client, response)
        return


@log
def process_message(message, names, listen_socks):
    if message[TO] in names and names[message[TO]] in listen_socks:
        send_msg(names[message[TO]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[TO]} '
                           f'от пользователя {message[FROM]}.')
    elif message[TO] in names and names[message[TO]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(
            f'Пользователь {message[TO]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


@log
def arg_parser():
    try:
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port = DEFAULT_PORT
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.error("При запуске клиента после параметра '-p' не указан номер порта.")
        sys.exit()
    except ValueError:
        SERVER_LOGGER.error('При запуске клиента неверно указан номер порта.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            address = sys.argv[sys.argv.index('-a') + 1]
        else:
            address = ''
    except IndexError:
        SERVER_LOGGER.error("При запуске клиента после параметра '-a' не указан адрес.")
        sys.exit(1)

    return port, address


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию
    :return:
    """
    port, address = arg_parser()

    SERVER_LOGGER.info(
        f'Запущен сервер, порт для подключений: {port}, '
        f'адрес с которого принимаются подключения: {address}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((address, port))
    sock.settimeout(0.5)

    clients = []
    messages = []

    names = dict()  # {client_name: client_socket}

    sock.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, addr = sock.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соедение с ПК {addr}')
            clients.append(client)

        r_clients = []
        w_clients = []

        try:
            if clients:
                r_clients, w_clients, _ = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if r_clients:
            for client_with_message in r_clients:
                try:
                    process_client_message(get_msg(client_with_message),
                                           messages, client_with_message, clients, names)
                except Exception:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                       f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения, обрабатываем каждое.
        for msg in messages:
            try:
                process_message(msg, names, w_clients)
                print('Сообщение отправлено')
            except Exception:
                SERVER_LOGGER.info(f'Связь с клиентом с именем {msg[TO]} была потеряна')
                clients.remove(names[msg[TO]])
                del names[msg[FROM]]
        messages.clear()


if __name__ == '__main__':
    main()
