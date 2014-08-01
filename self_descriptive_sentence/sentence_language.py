# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import abc
import itertools


class SentenceLanguage(object):
    _USER_TEXT_FIELD_NAME = 'user'
    _TOTAL_FIELD_NAME = 'total'
    _COUNTING_FIELD_NAME = 'counting'
    _CHARACTER_FIELD_NAME = 'char'
    _COUNT_FIELD_NAME = 'cnt'

    @abc.abstractmethod
    def is_countable_character(self, character):
        """
        :type character: unicode
        :rtype: bool
        """
        pass

    def tokenize(self, text):
        """
        :type text: unicode
        :rtype: collections.Iterable[unicode]
        """
        return itertools.ifilter(self.is_countable_character, text or '')

    @property
    @abc.abstractproperty
    def special_characters(self):
        """
        :rtype: collections.Iterable[unicode]
        """
        raise NotImplementedError

    @abc.abstractmethod
    def translate_number(self, number):
        """
        :type number: int | long
        :rtype: unicode
        """
        pass

    def compose_sentence(self, total_count, character_counts, user_text=None):
        """
        :type total_count: int
        :type character_counts: dict[unicode, int]
        :rtype: unicode
        """
        counting_text = ''.join([
            self._compose_character_count(character, count)
            for character, count in character_counts.iteritems()
            if count > 0
        ])

        params = {
            self._USER_TEXT_FIELD_NAME: user_text or '',
            self._TOTAL_FIELD_NAME: self.translate_number(total_count),
            self._COUNTING_FIELD_NAME: counting_text,
        }
        return self._sentence_template.format(**params)

    def get_single_use_template_text(self, user_text=''):
        """
        :rtype: unicode
        """
        params = {
            self._USER_TEXT_FIELD_NAME: user_text or '',
            self._TOTAL_FIELD_NAME: '',
            self._COUNTING_FIELD_NAME: '',
        }
        return self._sentence_template.format(**params)

    def get_repeated_template_text(self):
        """
        :rtype: unicode
        """
        params = {
            self._CHARACTER_FIELD_NAME: '',
            self._COUNT_FIELD_NAME: '',
        }
        return self._character_count_template.format(**params)

    @property
    @abc.abstractproperty
    def _sentence_template(self):
        """
        :rtype: unicode
        """
        raise NotImplementedError

    @property
    @abc.abstractproperty
    def _character_count_template(self):
        """
        :rtype: unicode
        """
        raise NotImplementedError

    def _compose_character_count(self, character, count):
        """
        :type character: unicode
        :type count: int
        :rtype: unicode
        """
        params = {
            self._CHARACTER_FIELD_NAME: character,
            self._COUNT_FIELD_NAME: self.translate_number(count),
        }
        return self._character_count_template.format(**params)
