import inspect
import json
import logging
import socket
import sys
import time

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
        CLIENT_LOGGER.info(f'Вызвана функция {func.__name__} с аргументами: {res}')
        CLIENT_LOGGER.info(f'Функция {func.__name__} вызвана из функции {code_obj_name}')
        return res

    return decorated


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


def main():
    try:
        server_adress = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_adress = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        CLIENT_LOGGER.info('error: номер порта должен быть в диапазоне от 1024 до 65535')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_adress, server_port))
    CLIENT_LOGGER.info(f'establish connection: {server_adress}: {server_port}')
    message_to_server = create_presence()
    CLIENT_LOGGER.info(f'message to server: {message_to_server}')
    send_message(transport, message_to_server)
    CLIENT_LOGGER.info('message send to server')
    try:
        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.info(f'answer: {answer}')
        print(answer)
    except (ValueError, json.JSONDecoder):
        CLIENT_LOGGER.info('error: сообщение не декодируется')


if __name__ == '__main__':
    main()
