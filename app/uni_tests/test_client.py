import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR
from client import process_ans
from common.variables import TIME
from client import create_presence
from common.variables import ACTION, USER, ACCOUNT_NAME, PRESENCE


class TestClient(unittest.TestCase):

    def test_create_presence_ok(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_ans_200_ok(self):
        test = process_ans({RESPONSE: 200})
        self.assertEqual(test, '200 : OK')

    def test_ans_400(self):
        test = process_ans({RESPONSE: 400, ERROR: 'Bad Request'})
        self.assertEqual(test, '400 : Bad Request')

    def test_no_response_message(self):
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
