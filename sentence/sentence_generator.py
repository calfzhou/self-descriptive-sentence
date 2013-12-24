#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from collections import OrderedDict
import copy
import random
import sys


class SentenceCount(OrderedDict):
    def __init__(self, *args, **kwargs):
        super(SentenceCount, self).__init__(*args, **kwargs)
        self.total = 0

    def update(self, arg=None, **kwargs):
        super(SentenceCount, self).update(arg, **kwargs)
        if isinstance(arg, SentenceCount):
            self.total += arg.total

    def clone(self):
        """
        :rtype: SentenceCount
        """
        return copy.copy(self)

    def __eq__(self, other):
        if isinstance(other, SentenceCount):
            if self.total != other.total:
                return False

            for character in self.viewkeys() | other.viewkeys():
                if self.get(character, 0) != other.get(character, 0):
                    return False

            return True

        return super(SentenceCount, self).__eq__(other)

    def __ne__(self, other):
        return not self == other

    def __unicode__(self):
        parts = ['{0}: {1}'.format(char, cnt) for char, cnt in self.iteritems() if cnt > 0]
        parts.append('{0}: {1}'.format('Total', self.total))
        return ', '.join(parts)

    def __str__(self):
        return unicode(self).encode(sys.getfilesystemencoding())


class Sentence(object):
    def __init__(self, language, user_text='', down_to_zero=None):
        """
        :type language: sentence_language.SentenceLanguage
        :type user_text: string
        :type down_to_zero: None|bool|random.Random
        :param down_to_zero: True to force decrease 2 to 0; False to force decrease 2 to 1;
                             A Random object to decrease 2 to 0 or 1 randomly.
                             None to use the module level random.
        """
        self._lang = language
        self._user_text = user_text
        self._repeated_template_characters = self._lang.tokenize(self._lang.repeated_template_text)

        if down_to_zero is None:
            self._need_down_to_zero = lambda: random.randint(0, 1) == 0
        elif down_to_zero is True:
            self._need_down_to_zero = lambda: True
        elif down_to_zero is False:
            self._need_down_to_zero = lambda: False
        elif isinstance(down_to_zero, random.Random):
            self._need_down_to_zero = lambda: down_to_zero.randint(0, 1) == 0
        else:
            raise ValueError('down_to_zero must be True, False, None, or a random.Random object')

        self._mutable_counts = SentenceCount()

        for character in self._lang.special_characters:
            self._mutable_counts[character] = 0

        self._prev_mutable_counts = self._mutable_counts.clone()

        map(lambda c: self._inc_character(c), self._lang.tokenize(self._user_text))
        map(lambda c: self._inc_character(c), self._lang.tokenize(self._lang.single_use_template_text))

    def is_finished(self):
        """
        :rtype: bool
        """
        return self._mutable_counts == self._prev_mutable_counts

    def evolve(self):
        older_counts = self._prev_mutable_counts
        self._prev_mutable_counts = self._mutable_counts.clone()

        self._replace_number(older_counts.total, self._prev_mutable_counts.total)

        for character in older_counts.viewkeys() | self._prev_mutable_counts.viewkeys():
            from_number = older_counts.get(character, 0)
            to_number = self._prev_mutable_counts.get(character, 0)
            self._replace_number(from_number, to_number)

    @property
    def counts(self):
        """
        :rtype: SentenceCount
        """
        return self._mutable_counts

    def _inc_character(self, character):
        """
        :type character: string
        """
        character_count = self._mutable_counts.get(character, 0)
        assert character_count >= 0, 'character count is negative'
        if character_count == 0:
            self._mutable_counts[character] = 2
            self._mutable_counts.total += 2
            map(lambda c: self._inc_character(c), self._repeated_template_characters)
        else:
            self._mutable_counts[character] += 1
            self._mutable_counts.total += 1

    def _dec_character(self, character):
        """
        :type character: string
        """
        assert self._mutable_counts[character] >= 2, 'character count is < 2'
        if self._mutable_counts[character] == 2 and self._need_down_to_zero():
            self._mutable_counts[character] -= 2
            self._mutable_counts.total -= 2
            map(lambda c: self._dec_character(c), self._repeated_template_characters)
        else:
            self._mutable_counts[character] -= 1
            self._mutable_counts.total -= 1

    def _replace_number(self, from_number, to_number):
        """
        :type from_number: int
        :type to_number: int
        """
        if from_number != to_number:
            if from_number > 0:
                map(lambda c: self._dec_character(c), self._lang.tokenize(self._lang.translate_number(from_number)))
            if to_number > 0:
                map(lambda c: self._inc_character(c), self._lang.tokenize(self._lang.translate_number(to_number)))


class SentenceGenerator(object):
    MAX_ATTEMPTS = 20
    MAX_ITERATIONS = 300

    @classmethod
    def generate(cls, language, user_text,
                 attempts=MAX_ATTEMPTS, iterations=MAX_ITERATIONS,
                 down_to_zero=None, verbose=True):
        """
        :type language: sentence_language.SentenceLanguage
        :type user_text: string
        :type attempts: int
        :type iterations: int
        :type down_to_zero: bool|object
        :param down_to_zero: True or False to set force decrease 2 to 0 or 1.
                             Otherwise, this parameter will be used to initialize a Random object.
        :type verbose: bool
        :rtype: SentenceCount|None
        """
        if not isinstance(down_to_zero, bool):
            down_to_zero = random.Random(down_to_zero)

        for attempt in xrange(attempts):
            if verbose:
                print('==================== ATTEMPT {} ===================='.format(attempt + 1), file=sys.stderr)

            sentence = Sentence(language, user_text=user_text, down_to_zero=down_to_zero)

            iteration = 0
            while True:
                if verbose:
                    print('[{}:{:3d}]'.format(attempt + 1, iteration), unicode(sentence.counts),
                          file=sys.stderr)

                if sentence.is_finished():
                    counts = sentence.counts
                    return counts

                iteration += 1
                if iteration > iterations:
                    break

                sentence.evolve()

            if isinstance(down_to_zero, bool):
                # If the behavior of decreasing 2 is determined, there is no need to do more attempts.
                break

        return None

    @classmethod
    def verify(cls, language, user_text, counts):
        """
        :type language: sentence_language.SentenceLanguage
        :type user_text: string
        :type counts: SentenceCount
        :rtype: bool
        """
        text = language.compose_sentence(counts.total, counts, user_text)
        actual_counts = SentenceCount()
        for character in language.tokenize(text):
            actual_counts.total += 1
            actual_counts[character] = actual_counts.get(character, 0) + 1

        return actual_counts == counts
