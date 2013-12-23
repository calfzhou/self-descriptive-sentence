DEMO
====

Some exmaple results:

- input `1`

2有2个1，4个2，1个3，2个4。

- input `3`

3有2个2，3个3。

- input `4`

4有3个2，2个3，2个4。

- input `13579`

13579有2个1，6个2，3个3，2个5，2个6，2个7，2个9。

BUG
===

There is a bug in the core logic.

If the first character processed by the loop inside `init` function is a special character,
the result is not a correct sentence.

The root cause is that `doinc` function cannot handle the case when the count of `个` is still zero.

This bug will be fixed in the master branch when rewriting this old code using Python.
