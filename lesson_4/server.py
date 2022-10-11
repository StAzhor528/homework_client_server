import json
import sys
from socket import AF_INET, SOCK_STREAM, socket
from common.utils import get_msg, send_msg
from common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, PRESENCE, TIME, \
    USER, ACCOUNT_NAME, RESPONSE, ERROR


def process_client_message(msg):
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
        print("После параметра '-p' не указан номер порта.")
        sys.exit()
    except ValueError:
        print('Номером порта может быть только число от 1024 до 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            address = sys.argv[sys.argv.index('-a') + 1]
        else:
            address = ''
    except IndexError:
        print("Не указан адрес после параметра '-a'")
        sys.exit(1)

    SOCKET = socket(AF_INET, SOCK_STREAM)
    SOCKET.bind((address, port))
    SOCKET.listen(MAX_CONNECTIONS)

    while True:
        CLIENT, ADDR = SOCKET.accept()
        try:
            msg_from_client = get_msg(CLIENT)
            print('Сообщение от клиента: ', msg_from_client)
            response = process_client_message(msg_from_client)
            send_msg(CLIENT, response)
            CLIENT.close()
        except (ValueError, json.JSONDecodeError):
            print('Некорректное сообщение от клиента')
            CLIENT.close()


if __name__ == '__main__':
    command_line_options()
