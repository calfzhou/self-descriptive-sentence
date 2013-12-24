Self-Descriptive Sentence
=========================

A self-descriptive sentence generator. Targeting on any languages.

Background
----------

What is a self-descriptive sentence?

Self-descriptive sentence, aka. **autogram**, is a sentence that describes itself in the sense of providing
an inventory of its own characters.

Here I'd like to show a famous example:

>   This sentence employs two a’s, two c’s, two d’s, twenty-eight e’s, five f’s, three g’s,
    eight h’s, eleven i’s, three l’s, two m’s, thirteen n’s, nine o’s, two p’s,
    five r’s, twenty-five s’s, twenty-three t’s, six v’s, ten w’s, two x’s, five y’s, and one z.

And another type:

>   T is the first, fourth, eleventh, sixteenth, ... letter in this sentence, not counting spaces or commas

For more information, please check [the Wikipedia page of Autogram](http://en.wikipedia.org/wiki/Autogram).

Purpose
-------

The purpose of this project is to build a program that could generate self-descriptive sentences.

As you may already known that there are several different types of **self-descriptive** (see above Wikipedia page).
Here in this project I will firstly focus on the self-counting one. This kind of self-descriptive will present,
for example, the total count of characters/words, the number of every single character/word, the number of
every punctuation, and also the number of spaces if you want.

Also, I don't want to limit my program on English sentences only. It should work on different languages with
minimal effort.

A Chinese self-counting sentence demo:

>   这个句子一共有七十五个字。其中有四个“十”；二个“子”；四个“三”；十二个“二”；二个“字”；一个“八”；三个“四”；
    一个“六”；二个“七”；二个“中”；二个“其”；二个“共”；二个“这”；二个“句”；五个“一”；二十二个“个”；三个“有”；
    一个“九”；三个“五”。

Program Usage
-------------

```
usage: self_descriptive_sentence.py [-h] [-v] [-a ATTEMPTS] [-i ITERATIONS]
                                    [-V] [-0 | -1 | -s SEED]
                                    [text]

Self-Descriptive Sentence Generator

positional arguments:
  text                  a text will be included in the sentence (default: )

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -a ATTEMPTS, --attempts ATTEMPTS
                        the maximum number of attempts (default: 20)
  -i ITERATIONS, --iterations ITERATIONS
                        the maximum number of iterations in each attempt
                        (default: 300)
  -V, --no-verbose      disable debug messages (default: False)
  -0, --down-to-zero    prefer zero when performing a decrease operation on a
                        count=2 character (default: False)
  -1, --down-to-one     prefer one when performing a decrease operation on a
                        count=2 character (default: False)
  -s SEED, --seed SEED  use a seeded Random object to randomly choose between
                        zero and one when performing a decrease operation on a
                        count=2 character (default: None)
```

Example
-------

`python self_descriptive_sentence.py -V`:

一共有四十八个字，二个“共”，二个“有”，二个“字”，三个“一”，七个“二”，四个“三”，三个“四”，二个“五”，二个“七”，二个“八”，一个“九”，三个“十”，十五个“个”。

`python self_descriptive_sentence.py -V 我写的这句话`:

我写的这句话一共有七十四个字，二个“我”，二个“写”，二个“的”，二个“这”，二个“句”，二个“话”，二个“共”，二个“有”，二个“字”，五个“一”，十三个“二”，三个“三”，四个“四”，二个“五”，二个“七”，一个“八”，一个“九”，四个“十”，二十一个“个”。
