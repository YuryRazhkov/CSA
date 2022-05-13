import inspect
import json
import logging
import socket
import sys
import logs.client_log_config

from common.utils import get_message, send_message
from common.variables import *

SERVER_LOGGER = logging.getLogger('serverapp')


def log(func):
    def decorated(*args, **kwargs):
        current_frame = inspect.currentframe()  # Текущий фрейм
        caller_frame = current_frame.f_back  # Следующий объект внешнего фрейма (вызывающий current_frame объект)
        code_obj = caller_frame.f_code  # Объект кода выполняемый в caller_frame
        code_obj_name = code_obj.co_name  # Имя, с которым был определён code_obj
        res = func(*args, **kwargs)
        SERVER_LOGGER.info(f'Вызвана функция {func.__name__} с аргументами: {res}')
        SERVER_LOGGER.info(f'Функция {func.__name__} вызвана из функции {code_obj_name}')
        return res

    return decorated


@log
def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message \
            and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


@log
def main():
    SERVER_LOGGER.info(f'start server')
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.error('error: enter port number')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.error('error: port number should be in range 1024-65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        SERVER_LOGGER.error('IndexError')
        sys.exit(1)

    SERVER_LOGGER.info('start server')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))

    transport.listen(MAX_CONNECTIONS)

    while True:

        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'establish connection: {client_address}')
        try:
            message_form_client = get_message(client)
            response = process_client_message(message_form_client)
            send_message(client, response)
            SERVER_LOGGER.info(f'message_form_client: {message_form_client};'
                               f'response: {response}')
            SERVER_LOGGER.info(f'close connection: {client_address}')
            client.close()
        except (ValueError, json.JSONDecoder):
            SERVER_LOGGER.error('error: bad massage')
            client.close()


if __name__ == '__main__':
    main()
