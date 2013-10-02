Promises is a very basic type checking library for Python.

.. code:: python

    from numbers import Number
    from promises import promise

    @promise.accepts(Number, Number)
    @promise.returns(Number)
    def add(a, b):
        return a + b

Of these example functions, `add` will work and `sub` will not. `add` expects two arguments of type `Number` and a return value of type `Number`. `sub` is impossible because