import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from client import create_answer, create_presence
from common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, STATUS, RESPONSE, ERROR


class TestClass(unittest.TestCase):
    def test_create_presence(self):
        answer = create_presence()
        answer[TIME] = 1
        self.assertEqual(answer, {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'Guest', STATUS: "Привет, я тут!"}})

    def test_create_answer_200(self):
        self.assertEqual(create_answer({RESPONSE: 200}), 'Все прошло без ошибок!')

    def test_create_answer_400(self):
        self.assertEqual(create_answer({RESPONSE: 400, ERROR: 'Bad Request'}), 'Ошибка!')

    def test_create_answer_value_error(self):
        self.assertRaises(ValueError, create_answer, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
