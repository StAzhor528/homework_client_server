"""Программа-клиент"""

import sys
import json
import socket
import time
import logging
import threading
import logs.config_client_log
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, ACTION, \
    TIME, USER, ACCOUNT_NAME, FROM, PRESENCE, RESPONSE, \
    ERROR, MESSAGE, MESSAGE_TEXT, TO, EXIT
from common.utils import get_msg, send_msg, log
from errors import IncorrectDataRecivedError, ReqFieldMissingError, ServerError

CLIENT_LOGGER = logging.getLogger('client')


@log
def create_exit_message(account_name):
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


@log
def message_from_server(sock, my_username):
    while True:
        try:
            message = get_msg(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    FROM in message and TO in message \
                    and MESSAGE_TEXT in message and message[TO] == my_username:
                print(f'\nПолучено сообщение от пользователя {message[FROM]}:'
                      f'\n{message[MESSAGE_TEXT]}')
                CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[FROM]}:'
                            f'\n{message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
        except IncorrectDataRecivedError:
            CLIENT_LOGGER.error(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
            break


@log
def create_message(sock, account_name='Guest'):
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        ACTION: MESSAGE,
        FROM: account_name,
        TO: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_msg(sock, message_dict)
        CLIENT_LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
    except Exception as e:
        print(e)
        CLIENT_LOGGER.critical('Потеряно соединение с сервером.')
        sys.exit(1)


@log
def user_interactive(sock, username):
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_msg(sock, create_exit_message(username))
            print('Завершение соединения.')
            CLIENT_LOGGER.info('Завершение работы по команде пользователя.')

            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


@log
def create_presence(account_name):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


def print_help():
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log
def process_response_ans(msg):
    CLIENT_LOGGER.debug(f'Разбор приветственного сообщения от сервера: {msg}')
    if RESPONSE in msg:
        if msg[RESPONSE] == 200:
            return '200 : OK'
        elif msg[RESPONSE] == 400:
            raise ServerError(f'400 : {msg[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


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

    try:
        if '-n' in sys.argv:
            name = sys.argv[sys.argv.index('-n') + 1]
        else:
            name = None
    except IndexError:
        CLIENT_LOGGER.error("При запуске клиента после параметра '-n' не указано имя.")
        sys.exit(1)

    return port, address, name


def main():
    port, address, name = arg_parser()

    print(f'Консольный месседжер. Клиентский модуль. Имя пользователя: {name}')

    if not name:
        name = input('Введите имя пользователя: ')

    CLIENT_LOGGER.info(
        f'Запущен клиент с параметрами: адрес сервера: {address}, '
        f'порт: {port}, имя пользователя: {name}')

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, port))
        send_msg(sock, create_presence(name))
        answer = process_response_ans(get_msg(sock))
        CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except (ConnectionRefusedError, ConnectionError):
        CLIENT_LOGGER.critical(
            f'Не удалось подключиться к серверу {address}:{port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        receiver = threading.Thread(target=message_from_server, args=(sock, name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(sock, name))
        user_interface.daemon = True
        user_interface.start()
        CLIENT_LOGGER.debug('Запущены процессы')

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
