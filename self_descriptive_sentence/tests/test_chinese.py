# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
from os import path
import unittest
from self_descriptive_sentence.chinese import Chinese


class TestChineseNumber(unittest.TestCase):
    RESOURCES_PATH = path.join(path.dirname(path.abspath(__file__)), 'resources')

    def setUp(self):
        self.number_data_path = 'number_data.txt'
        self.chinese = Chinese()

    def test_zero(self):
        self.assertEqual(self.chinese.translate_number(0), '零')

    @staticmethod
    def create_number_test_method(number, expected):
        """
        :type number: int | long
        :type expected: unicode
        :rtype: (TestChineseNumber) -> None
        """
        def _test_method(self):
            """
            :type self: TestChineseNumber
            """
            actual_positive = self.chinese.translate_number(number)
            self.assertEqual(actual_positive, expected)

            actual_negative = self.chinese.translate_number(-number)
            self.assertEqual(actual_negative, '负{0}'.format(expected))

        return _test_method

    @classmethod
    def add_data_driven_tests(cls):
        number_data_path = path.join(cls.RESOURCES_PATH, 'number_data.txt')
        with codecs.open(number_data_path, encoding='utf-8') as data_file:
            for line in data_file:
                line = line.rstrip('\r\n')
                number_text, expected = line.split('\t')
                number = int(number_text)
                setattr(TestChineseNumber, 'test_number_{0}'.format(number),
                        cls.create_number_test_method(number, expected))


TestChineseNumber.add_data_driven_tests()


if __name__ == '__main__':
    unittest.main()
    pass
