import inspect
import json
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))

import logs.client_log_config
import logs.server_log_config


from .variables import MAX_PACKAGE_LENGHT, ENCODING

def log(func):


    def decorated(*args, **kwargs):

        logger_name = 'serverapp' if 'server.py' in sys.argv[0] else 'clientapp'
        LOGGER = logging.getLogger(logger_name)

        current_frame = inspect.currentframe()  # Текущий фрейм
        caller_frame = current_frame.f_back  # Следующий объект внешнего фрейма (вызывающий current_frame объект)
        code_obj = caller_frame.f_code  # Объект кода выполняемый в caller_frame
        code_obj_name = code_obj.co_name  # Имя, с которым был определён code_obj
        res = func(*args, **kwargs)
        LOGGER.info(f'Вызвана функция {func.__name__} с аргументами: {args} {kwargs}')
        LOGGER.info(f'Функция {func.__name__} вызвана из функции {code_obj_name}')
        return res

    return decorated


@log
def get_message(client):
    encoder_responce = client.recv(MAX_PACKAGE_LENGHT)
    if isinstance(encoder_responce, bytes):
        json_response = encoder_responce.decode(ENCODING)
        if isinstance(json_response, str):
            responce = json.loads(json_response)
            if isinstance(responce, dict):
                return responce
            raise ValueError
        raise ValueError
    raise ValueError


@log
def send_message(sock, message):
    if not isinstance(message, dict):
        raise TypeError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
