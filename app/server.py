import json
import socket
import sys

from common.utils import get_message, send_message
from common.variables import *



def process_client_message(message):

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message \
            and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():


    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('enter port number')
        sys.exit(1)
    except ValueError:
        print('port number should be in range 1024-65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))

    transport.listen(MAX_CONNECTIONS)

    while True:

        client, client_address = transport.accept()
        try:
            message_form_client = get_message(client)
            response = process_client_message(message_form_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecoder):
            print('bad massage')
            client.close()


if __name__ == '__main__':
    main()
