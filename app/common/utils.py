import json


from .variables import MAX_PACKAGE_LENGHT, ENCODING


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


def send_message(sock, message):
    if not isinstance(message, dict):
        raise TypeError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
