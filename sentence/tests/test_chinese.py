# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import unittest
from chinese import Chinese


class TestChineseNumber(unittest.TestCase):
    def setUp(self):
        self.number_data_path = 'number_data.txt'
        self.chinese = Chinese()

    def test_zero(self):
        self.assertEqual(self.chinese.translate_number(0), '零')


def create_number_test_func(number, expected):
    def _test_func(self):
        actual_positive = self.chinese.translate_number(number)
        self.assertEqual(actual_positive, expected)

        actual_negative = self.chinese.translate_number(-number)
        self.assertEqual(actual_negative, '负{0}'.format(expected))

    return _test_func


def add_data_driven_tests():
    number_data_path = 'number_data.txt'
    with open(number_data_path) as data_file:
        for line in data_file:
            line = line.decode('utf8')
            line = line.rstrip('\r\n')
            number_text, expected = line.split('\t')
            number = int(number_text)
            setattr(TestChineseNumber, 'test_number_{0}'.format(number),
                    create_number_test_func(number, expected))


add_data_driven_tests()


if __name__ == '__main__':
    unittest.main()
    pass
