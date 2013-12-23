DEMO
====

Some exmaple results:

- input `empty`

这个句子一共有六十八个字。其中有：二个“这”；二个“句”；二个“子”；二个“共”；三个“有”；二个“字”；二个“其”；二个“中”；二十个“个”；三个“一”；十二个“二”；四个“三”；三个“四”；二个“六”；二个“八”；一个“九”；四个“十”。

- input `计算机生成的`

计算机生成的这个句子一共有九十六个字。其中有：二个“计”；二个“算”；二个“机”；二个“生”；二个“成”；二个“的”；二个“这”；二个“句”；二个“子”；二个“共”；三个“有”；二个“字”；二个“其”；二个“中”；二十七个“个”；三个“一”；十七个“二”；四个“三”；四个“四”；一个“五”；二个“六”；三个“七”；二个“九”；四个“十”。

BUG
===

There is a bug in the core logic.

If the first character processed by the loop inside `init` function is a special character,
the result is not a correct sentence.

The root cause is that `doinc` function cannot handle the case when the count of `个` is still zero.

This bug will be fixed in the master branch when rewriting this old code using Python.
