Promises is a very basic type checking library for Python.

.. code:: python

    from numbers import Number
    from promises import promise

    @promise.returns(str)
    def add(a, b):
        return a + b

    @promise.accepts(Number, Number)
    @promise.returns(Number)
    def sub(a, b):
        return a - b

    sub(5, 2)        # works
    sub('5', '2')    # raises TypeError

    add('Hel', 'lo') # works
    add(1, 2)        # raises ReturnError