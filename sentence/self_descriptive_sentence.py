#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import argparse
import sys
import chinese
import number
from sentence_generator import SentenceGenerator

__version__ = '0.1'
__author__ = 'calf.zhou@gmail.com'


def main():
    parser = argparse.ArgumentParser(
        description='Self-Descriptive Sentence Generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        version=__version__
    )
    parser.add_argument('text', nargs='?', default='', help='a text will be included in the sentence')
    parser.add_argument('-l', '--language', default='chinese', choices=('chinese', 'number'),
                        help='choose a language to generate sentence')

    parser.add_argument('-a', '--attempts', type=int, default=SentenceGenerator.MAX_ATTEMPTS,
                        help='the maximum number of attempts')
    parser.add_argument('-i', '--iterations', type=int, default=SentenceGenerator.MAX_ITERATIONS,
                        help='the maximum number of iterations in each attempt')
    parser.add_argument('-V', '--no-verbose', action='store_true',
                        help='disable debug messages')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-0', '--down-to-zero', action='store_true',
                       help='prefer zero when performing a decrease operation on a count=2 character')
    group.add_argument('-1', '--down-to-one', action='store_true',
                       help='prefer one when performing a decrease operation on a count=2 character')
    group.add_argument('-s', '--seed', type=int,
                       help='use a seeded Random object to randomly choose between zero and one'
                            ' when performing a decrease operation on a count=2 character')

    unicode_args = map(lambda s: unicode(s, sys.getfilesystemencoding()), sys.argv)
    args = parser.parse_args(unicode_args[1:])

    if args.down_to_zero:
        down_to_zero = True
    elif args.down_to_one:
        down_to_zero = False
    else:
        down_to_zero = args.seed

    if args.language == 'chinese':
        language = chinese.Chinese()
    elif args.language == 'number':
        language = number.Number()
    else:
        raise ValueError('unknown language {}'.format(args.language))

    counts = SentenceGenerator.generate(language, user_text=args.text,
                                        attempts=args.attempts, iterations=args.iterations,
                                        down_to_zero=down_to_zero, verbose=not args.no_verbose)
    if counts:
        print(language.compose_sentence(counts.total, counts, user_text=args.text))
        if not SentenceGenerator.verify(language, args.text, counts):
            raise Exception('Oops, something is wrong, we got an incorrect sentence!')
    else:
        print('Generation failed.')


if __name__ == '__main__':
    main()
