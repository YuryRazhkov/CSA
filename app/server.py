import datetime
import inspect
import json
import logging
import select
import socket
import sys
import time
from pprint import pprint

import logs.server_log_config

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
        SERVER_LOGGER.info(f'Вызвана функция {func.__name__} с аргументами: {args} {kwargs}')
        SERVER_LOGGER.info(f'Функция {func.__name__} вызвана из функции {code_obj_name}')
        return res

    return decorated


@log
def process_client_message(message, messages_list, client):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клинта,
    проверяет корректность, отправляет словарь-ответ для клиента с результатом приёма.
    :param message:
    :param messages_list:
    :param client:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    # Если это сообщение о присутствии, принимаем и отвечаем, если успех
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    # Иначе отдаём Bad request
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


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
    transport.settimeout(0.5)
    transport.listen(MAX_CONNECTIONS)


    clients = []
    messages = []

    while True:
        try:
            client, client_address = transport.accept()
        except OSError as err:
            print(err.errno, '--',  time.asctime())
            pass
        else:
            SERVER_LOGGER.info(f'connected {client_address}')
            print(time.asctime(), 'conected', client_address)
            clients.append(client)


        recv_data_lst = []
        send_data_lst = []
        err_lst = []


        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)

        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
