import sys
from socket import AF_INET, SOCK_STREAM, socket
from utils import send_msg, get_msg
from datetime import datetime


def command_line_options():
    try:
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port = 7777
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
    SOCKET.connect(('localhost', port))
    MSG = {"action": "presence",
           "time": str(datetime.now()),
           "type": "status",
           "user": {"account_name": "Ivan",
                    "status": "Привет, я тут!"
                    }
           }

    send_msg(SOCKET, MSG)
    response = get_msg(SOCKET)
    if response['response'] == 200:
        print('Все прошло без ошибок!')
    else:
        print('Ошибка!')

    SOCKET.close()

if __name__ == '__main__':
    command_line_options()