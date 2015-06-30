Title: GSoC'15: Mixing both assumption systems, Midterm updates
Date: 2015-07-01 03:30
Category: GSoC
Tags: python, sympy, gsoc
Slug: gsoc15-midterm-updates
Author: Sudhanshu Mishra


It's been very long since I've written anything here. Here's some of the pull requests that I've created during this period:

* [Q.nonzero(non-real) now returns False](https://github.com/sympy/sympy/pull/9490) Now `Q.nonzero` requires the argument to be real along with nonzero to return `True`.

* [Make nonzero -> real & !zero like new assumptions](https://github.com/sympy/sympy/pull/9582) This PR proposes the same change for old assumptions which has been mentioned earlier.

* [An attempt to make zero an imaginary number](https://github.com/sympy/sympy/pull/9583) To make both the systems consistent, this PR proposes to make `0` an imaginary number in the old assumptions.

* [Add few more facts to satask](https://github.com/sympy/sympy/pull/9562) Now things like `satask(Q.negative(x + y), Q.positive(x) & Q.positive(y))` work. The `known_facts` was missing `Implies(Q.positive, ~Q.negative)`.

* [Proof of concept[1]: New assumptions check old assumptions for Symbol](https://github.com/sympy/sympy/pull/9560) This PR enables new assumptions to read the assumptions set over `Symbol` by changing the ask handlers.

* [Proof of concept[2]: New assumptions check old assumptions for Symbol](https://github.com/sympy/sympy/pull/9561) This PR enables new assumptions to read the assumptions set over `Symbol` by changing the satask handlers.

There's also this patch which makes changes in the `Symbol` itself to make this work.

```diff
commit de49998cc22c1873799539237d6202134a463956
Author: Sudhanshu Mishra <mrsud94@gmail.com>
Date:   Tue Jun 23 16:35:13 2015 +0530

    Symbol creation adds provided assumptions to global assumptions

diff --git a/sympy/core/symbol.py b/sympy/core/symbol.py
index 3945fa1..45be26d 100644
--- a/sympy/core/symbol.py
+++ b/sympy/core/symbol.py
@@ -96,8 +96,41 @@ def __new__(cls, name, **assumptions):
         False

         """
+        from sympy.assumptions.assume import global_assumptions
+        from sympy.assumptions.ask import Q
+
         cls._sanitize(assumptions, cls)
-        return Symbol.__xnew_cached_(cls, name, **assumptions)
+        sym = Symbol.__xnew_cached_(cls, name, **assumptions)
+
+        items_to_remove = []
+        # Remove previous assumptions on the symbol with same name.
+        # Note: This doesn't check expressions e.g. Q.real(x) and
+        # Q.positive(x + 1) are not contradicting.
+        for assumption in global_assumptions:
+            if isinstance(assumption.arg, cls):
+                if str(assumption.arg) == name:
+                    items_to_remove.append(assumption)
+
+        for item in items_to_remove:
+            global_assumptions.remove(item)
+
+        for key, value in assumptions.items():
+            if not hasattr(Q, key):
+                continue
+            # Special case to handle commutative key as this is true
+            # by default
+            if key == 'commutative':
+                if not assumptions[key]:
+                    global_assumptions.add(~getattr(Q, key)(sym))
+                continue
+
+            if value:
+                global_assumptions.add(getattr(Q, key)(sym))
+            elif value is False:
+                global_assumptions.add(~getattr(Q, key)(sym))
+
+        return sym
+

     def __new_stage2__(cls, name, **assumptions):
         if not isinstance(name, string_types):


Master

In [1]: from sympy import *
In [2]: %time x = Symbol('x', positive=True, real=True, integer=True)
CPU times: user 233 µs, sys: 29 µs, total: 262 µs
Wall time: 231 µs


This branch

In [1]: from sympy import *
In [2]: %time x = Symbol('x', positive=True, real=True, integer=True)
CPU times: user 652 µs, sys: 42 µs, total: 694 µs
Wall time: 657 µs
```

I did a small benchmarking by creating 100 symbols and setting assumptions over them and then later asserting them. It turns out that the one with changes in the ask handers is performing better than the other two.

Here's the report of the benchmarking:

When Symbol is modified
-----------------------

```
Line #    Mem usage    Increment   Line Contents
================================================
     6     30.2 MiB      0.0 MiB   @profile
     7                             def mem_test():
     8     30.5 MiB      0.3 MiB       _syms = [Symbol('x_' + str(i), real=True, positive=True) for i in range(1, 101)]
     9     34.7 MiB      4.2 MiB       for i in _syms:
    10     34.7 MiB      0.0 MiB           assert ask(Q.positive(i)) is True
```

[pyinstrument report](https://www.dropbox.com/s/ndujng8drhouj4v/sym_mod.html?dl=0)


When ask handlers are modified
------------------------------

```
Line #    Mem usage    Increment   Line Contents
================================================
     6     30.2 MiB      0.0 MiB   @profile
     7                             def mem_test():
     8     30.4 MiB      0.2 MiB       _syms = [Symbol('x_' + str(i), real=True, positive=True) for i in range(1, 101)]
     9     31.5 MiB      1.1 MiB       for i in _syms:
    10     31.5 MiB      0.0 MiB           assert ask(Q.positive(i)) is True
```

[pyinstrument report](https://www.dropbox.com/s/6823wp6iob4zjg5/ask_mod.html?dl=0)


When satask handlers are modified
---------------------------------

```
Line #    Mem usage    Increment   Line Contents
================================================
     6     30.2 MiB      0.0 MiB   @profile
     7                             def mem_test():
     8     30.4 MiB      0.2 MiB       _syms = [Symbol('x_' + str(i), real=True, positive=True) for i in range(1, 101)]
     9     41.1 MiB     10.7 MiB       for i in _syms:
    10     41.1 MiB      0.0 MiB           assert ask(Q.positive(i)) is True
```

[pyinstrument report](https://www.dropbox.com/s/l6a0037m6rxj84v/satask_mod.html?dl=0)


On the other hand, the [documentation PR](https://github.com/sympy/sympy/pull/9475) is almost ready to go.

As of now I'm working on fixing the inconsistencies between the two assumption systems. After that I'll move to reduce autosimplification based on the assumptions in the core.

That's all for now. Cheers!
