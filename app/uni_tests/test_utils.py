import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.utils import send_message, get_message
from common.variables import ENCODING, RESPONSE, ERROR


class TestSocket:

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.recevived_message = None

    def send(self, message):
        js_test_message = json.dumps(self.test_dict)
        self.encoded_message = js_test_message.encode(ENCODING)
        self.recevived_message = message

    def recv(self, max_len):
        js_test_message = json.dumps(self.test_dict)
        return js_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    test_dict = {'ACTION': 'PRESENCE', 'TIME': 1.1, 'USER': {'ACCOUNT_NAME': 'Guest'}}
    test_dict_recive_ok = {RESPONSE: 200}
    test_dict_recive_err = {RESPONSE: 400, ERROR: 'Bad Request'}

    def test_send_message_ok(self):
        test_socket = TestSocket(self.test_dict)
        send_message(test_socket, self.test_dict)
        self.assertEqual(test_socket.encoded_message, test_socket.recevived_message)

    def test_test_send_message_with_error(self):
        test_socket = TestSocket(self.test_dict)
        send_message(test_socket, self.test_dict)
        self.assertRaises(TypeError, send_message, test_socket, 'some string, not dict')

    def test_get_message_ok(self):
        test_socket_ok = TestSocket(self.test_dict_recive_ok)
        self.assertEqual(get_message(test_socket_ok), self.test_dict_recive_ok)

    def test_get_message_wrong(self):
        test_socket_ok = TestSocket(self.test_dict_recive_err)
        self.assertEqual(get_message(test_socket_ok), self.test_dict_recive_err)


if __name__ == '__main__':
    unittest.main()
