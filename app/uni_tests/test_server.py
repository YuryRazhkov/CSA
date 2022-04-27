import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR
from server import process_client_message
from common.variables import ACTION, USER, ACCOUNT_NAME, PRESENCE, TIME


class TestServer(unittest.TestCase):

    def test_process_client_message_ok(self):
        test = process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})
        self.assertEqual(test, {RESPONSE: 200})

    def test_process_client_message_no_user(self):
        test = process_client_message({ACTION: PRESENCE, TIME: 1.1})
        self.assertEqual(test, {RESPONSE: 400, ERROR: 'Bad Request'})

    def test_process_client_message_no_time(self):
        test = process_client_message({ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}})
        self.assertEqual(test, {RESPONSE: 400, ERROR: 'Bad Request'})

    def test_process_client_message_no_action(self):
        test = process_client_message({TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})
        self.assertEqual(test, {RESPONSE: 400, ERROR: 'Bad Request'})

    def test_process_client_message_wrong_user(self):
        test = process_client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Goose'}})
        self.assertEqual(test, {RESPONSE: 400, ERROR: 'Bad Request'})

    def test_process_client_message_wrong_action(self):
        test = process_client_message({ACTION: 'NO_PRESENCE', TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})
        self.assertEqual(test, {RESPONSE: 400, ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
