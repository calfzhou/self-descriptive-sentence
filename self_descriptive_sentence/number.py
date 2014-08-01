# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import itertools
from sentence_language import SentenceLanguage


class Number(SentenceLanguage):
    def __init__(self):
        super(Number, self).__init__()

        self.__sentence_template = '{{{user}}} employs {{{total}}} digits{{{counting}}}.'.format(
            user=self._USER_TEXT_FIELD_NAME, total=self._TOTAL_FIELD_NAME, counting=self._COUNTING_FIELD_NAME
        )
        """:type: unicode"""
        self.__character_count_template = ', {{{count}}} {{{char}}}\'s'.format(
            count=self._COUNT_FIELD_NAME, char=self._CHARACTER_FIELD_NAME
        )
        """:type: unicode"""

    def is_countable_character(self, character):
        """
        :type character: unicode
        :rtype: bool
        """
        return character and ('0' <= character <= '9')

    @property
    def special_characters(self):
        """
        :rtype: collections.Iterable[unicode]
        """
        return itertools.imap(str, xrange(10))

    def translate_number(self, number):
        """
        :type number: int | long
        :rtype: unicode
        """
        if not isinstance(number, (int, long)):
            raise ValueError('number must be integer')

        return unicode(number)

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

