BUG
===

There is a bug in the core logic.

If the first character processed by the loop inside `init` function is a special character,
the result is not a correct sentence.

The root cause is that `doinc` function cannot handle the case when the count of `个` is still zero.

This bug will be fixed in the master branch when rewriting this old code using Python.
