import argparse
import inspect
import json
import logging
import socket
import sys
import time
import logs.client_log_config

from common.utils import send_message, get_message
from common.variables import *

CLIENT_LOGGER = logging.getLogger('clientapp')


def log(func):
    def decorated(*args, **kwargs):
        current_frame = inspect.currentframe()  # Текущий фрейм
        caller_frame = current_frame.f_back  # Следующий объект внешнего фрейма (вызывающий current_frame объект)
        code_obj = caller_frame.f_code  # Объект кода выполняемый в caller_frame
        code_obj_name = code_obj.co_name  # Имя, с которым был определён code_obj
        res = func(*args, **kwargs)
        CLIENT_LOGGER.info(f'Вызвана функция {func.__name__} с аргументами: {args} {kwargs}')
        CLIENT_LOGGER.info(f'Функция {func.__name__} вызвана из функции {code_obj_name}')
        return res

    return decorated


@log
def create_message(sock, account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
        }
    }
    return out


@log
def process_ans(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    CLIENT_LOGGER.error('error: no RESPONSE in message')
    raise ValueError

@log
def arg_parser():
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='send', nargs='?')
    print(parser)

    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode
    print(client_mode)

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, '
                        f'допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode

def main():
    server_address, server_port, client_mode = arg_parser()

    CLIENT_LOGGER.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
        f'порт: {server_port}, режим работы: {client_mode}')

    try:


        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        CLIENT_LOGGER.info(f'establish connection: {server_address}: {server_port}')
        message_to_server = create_presence()
        CLIENT_LOGGER.info(f'message to server: {message_to_server}')
        send_message(transport, message_to_server)
        CLIENT_LOGGER.info('message send to server')

    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)

    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        print('Режим работы - отправка сообщений.')

        while True:
            try:
                send_message(transport, create_message(transport))
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                sys.exit(1)




if __name__ == '__main__':
    main()
