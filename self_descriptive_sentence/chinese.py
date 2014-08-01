# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sentence_language import SentenceLanguage
import utils


class Chinese(SentenceLanguage):
    CHINESE_NEGATIVE = '负'
    CHINESE_ZERO = '零'
    CHINESE_DIGITS = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    CHINESE_UNITS = ['', '十', '百', '千']
    CHINESE_GROUP_UNITS = ['', '万', '亿', '兆']

    def __init__(self):
        super(Chinese, self).__init__()

        self.__sentence_template = '{{{user}}}一共有{{{total}}}个字{{{counting}}}。'.format(
            user=self._USER_TEXT_FIELD_NAME, total=self._TOTAL_FIELD_NAME, counting=self._COUNTING_FIELD_NAME
        )
        """:type: unicode"""
        self.__character_count_template = '，{{{count}}}个“{{{char}}}”'.format(
            count=self._COUNT_FIELD_NAME, char=self._CHARACTER_FIELD_NAME
        )
        """:type: unicode"""

        self._list_of_special_chars = []
        """:type: list[unicode]"""

        self._add_special_char(self.CHINESE_ZERO)
        for character in self.CHINESE_DIGITS:
            self._add_special_char(character)
        for character in self.CHINESE_UNITS:
            self._add_special_char(character)

    def _add_special_char(self, character):
        """
        :rtype character: string
        """
        if self.is_countable_character(character):
            self._list_of_special_chars.append(character)

    def is_countable_character(self, character):
        """
        :type character: string
        :rtype: bool
        """
        return ('\u4e00' <= character <= '\u9fff') if character else False

    @property
    def special_characters(self):
        """
        :rtype: collections.Iterable[unicode]
        """
        return self._list_of_special_chars

    def translate_number(self, number):
        """
        :type number: int|long
        :rtype: unicode
        """
        if not isinstance(number, int) and not isinstance(number, long):
            raise ValueError('number must be integer')

        if number == 0:
            return self.CHINESE_ZERO

        words = []

        if number < 0:
            words.append(self.CHINESE_NEGATIVE)
            number = -number

        group_is_zero = True
        need_zero = False
        for position, digit in reversed(list(utils.enumerate_digits(number))):
            unit = position % len(self.CHINESE_UNITS)
            group = position // len(self.CHINESE_UNITS)

            if digit != 0:
                if need_zero:
                    words.append(self.CHINESE_ZERO)

                if digit != 1 or unit != 1 or not group_is_zero or (group == 0 and need_zero):
                    words.append(self.CHINESE_DIGITS[digit])

                words.append(self.CHINESE_UNITS[unit])

            group_is_zero = group_is_zero and digit == 0

            if unit == 0 and not group_is_zero:
                words.append(self.CHINESE_GROUP_UNITS[group])

            need_zero = (digit == 0 and (unit != 0 or group_is_zero))

            if unit == 0:
                group_is_zero = True

        return ''.join(words)

    @property
    def _sentence_template(self):
        """
        :rtype: unicode
        """
        return self.__sentence_template

    @property
    def _character_count_template(self):
        """
        :rtype: unicode
        """
        return self.__character_count_template
