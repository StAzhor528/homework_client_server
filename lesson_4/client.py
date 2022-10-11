import json
import sys
from socket import AF_INET, SOCK_STREAM, socket
from common.utils import send_msg, get_msg
from datetime import datetime
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, PRESENCE, ACTION, \
    ACCOUNT_NAME, TIME, USER, RESPONSE, STATUS


def create_presence(account_name='Guest'):
    msg = {ACTION: PRESENCE,
           TIME: str(datetime.now()),
           USER: {ACCOUNT_NAME: account_name,
                  STATUS: "Привет, я тут!"
                  }
           }
    return msg


def create_answer(msg):
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
        print("После параметра '-p' не указан номер порта.")
        sys.exit()
    except ValueError:
        print('Номером порта может быть только число от 1024 до 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            address = sys.argv[sys.argv.index('-a') + 1]
        else:
            address = DEFAULT_IP_ADDRESS
    except IndexError:
        print("Не указан адрес после параметра '-a'")
        sys.exit(1)

    SOCKET = socket(AF_INET, SOCK_STREAM)
    SOCKET.connect((address, port))
    msg = create_presence()
    send_msg(SOCKET, msg)

    try:
        answer = create_answer(get_msg(SOCKET))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение')

    SOCKET.close()


if __name__ == '__main__':
    command_line_options()
