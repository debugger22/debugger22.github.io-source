Title: Google Summer of Code 2015 with SymPy
Date: 2015-05-01 11:00
Category: GSoC
Tags: python, sympy, gsoc
Slug: gsoc15-with-sympy
Author: Sudhanshu Mishra

<p align="center">
<img src="{filename}/images/gsoc15.png" />
</p>

Once again I got accepted into Google Summer of Code! I'll be working on assumptions system of SymPy. This time, SymPy is participating under Python Software Foundation.

<p align="center">
<img src="{filename}/images/sympy.png" />
</p>

*SymPy is a Python library for symbolic mathematics. It aims to become a full-featured [Computer Algebra System](https://en.wikipedia.org/wiki/Computer_algebra_system) while keeping the code as simple as possible in order to be comprehensible and easily extensible.*

Here's what ideas page says about the project:

<div style="border:1px solid #C74350;padding:10px;border-radius: 5px;">
<i>
The project is to completely remove our old assumptions system, replacing it
with the new one.<br/><br/>

The difference between the two systems is outlined in the first two sections of this blog post.  A list of detailed issues can be found at this issue.<br/><br/>

This project is challenging.  It requires deep understanding of the core of SymPy, basic logical inference, excellent code organization, and attention to performance.  It is also very important and of high value to the SymPy community.<br/><br/>

You should take a look at the work started at
<a href="https://github.com/sympy/sympy/pull/2508">https://github.com/sympy/sympy/pull/2508</a>. Numerous related tasks are mentioned in the "Ideas" section.
</i>
</div>
My mentors are [Aaron Meurer](https://github.com/asmeurer) and [Tim Lahey](https://github.com/tjl).

Currently SymPy has two versions of mathematical assumptions. One is called "old assumptions" because a new implementation has been carried out recently. Since "old assumptions" were developed a long back, they are more mature and faster. However, because of its design, it is not capable of doing some interesting things like assuming something over an expression e.g. `x**2 + 2 > 0`.

Old assumptions store assumptions in the object itself. For example, the code `x = Symbol('x', finite=True)` will store the assumption that the `x` is finite in this object itself.

Both systems expose different APIs to query the facts:

Old:

```python
In [1]: from sympy import *

In [2]: x = Symbol('x', imaginary=True)

In [3]: x.is_real
Out[3]: False
```

New:

```python
In [4]: y = Symbol('y')

In [5]: ask(Q.real(y), Q.positive(y))
Out[5]: True
```

My work includes but is not limited to:

* Identifying inconsistencies between old and new assumptions and eliminate them.
* Improving performance of the new assumptions.
* Making new assumptions read old assumptions.
* Removing assumptions from the core as much as possible.
* Making API of old assumptions call new assumptions internally.

That's all for now. Looking forward to a great summer!
