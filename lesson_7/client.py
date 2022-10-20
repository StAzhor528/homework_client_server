import sys
import logging
import logs.client_log_config
from socket import AF_INET, SOCK_STREAM, socket
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ENCODING, MAX_PACKAGE_LENGTH, DEFAULT_CLIENT_MODE

CLIENT_LOGGER = logging.getLogger('client')


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

    try:
        if '-m' in sys.argv:
            mode = sys.argv[sys.argv.index('-m') + 1]
        else:
            mode = DEFAULT_CLIENT_MODE
    except IndexError:
        CLIENT_LOGGER.error("При запуске клиента после параметра '-m' не указан режим работы.")
        sys.exit(1)

    if mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {mode}, допустимые режимы: listen , send')
        sys.exit(1)
    print('Клиент для передачи сообщения') if mode == 'send' else print('Клиент для приема сообщения\n'
                                                                        'Кто присылает: Сообщение')
    CLIENT_LOGGER.info(f'Попытка подсоединения к серверу со стороны клиента.'
                       f'Порт для подключений: {port}'
                       f'Адрес подключения: {address}')

    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((address, port))
        while True:
            if mode == 'send':
                msg = ''

                while msg.strip() == '':
                    msg = input('Введите сообщение: ')
                if msg == 'exit':
                    break
                sock.send(msg.encode(ENCODING))
            else:

                answer = sock.recv(MAX_PACKAGE_LENGTH).decode(ENCODING)
                print(f'{answer}')


if __name__ == '__main__':
    command_line_options()
