MUST_RETURN_TYPE_SINGULAR = "Function `{0}` must return type {1}"
MUST_RETURN_TYPE_PLURAL = "Function `{0}` must return one of these types: {1}"
MUST_BE_OF_TYPE_SINGULAR = "Argument {0} to function `{1}` must be of type {2}"
MUST_BE_OF_TYPE_PLURAL =  "Argument {0} to function `{1}` must be one of these types: {2}"



INT = int, long,
DEC = float,
NUM = INT + DEC + (complex,)
TEXT = str, unicode,
SEQ = str, unicode, list, tuple, bytearray, buffer, xrange,
SET = set, frozenset,
MAP = dict,
ITER = SEQ + SET + MAP,


class ReturnException(Exception):
    pass


def type_name(t):
    if isinstance(t, ITER):
        return map(lambda x: x.__name__, t)
    else:
        return t.__name__


def accepts(*arg_types, **kwarg_types):
    """
    Decorator to add parameter type-checking to functions.

    Look at the libraries `collections`, `numbers`, and `types`.
    """
    def outer_wrapper(f):
        def inner_wrapper(*args, **kwargs):
            #verify positional args
            args_n_types = zip(args, arg_types)
            i = 0
            for at in args_n_types:
                if at[1] is not None and not isinstance(at[0], at[1]):
                    if len(at[1]) > 2:
                        raise TypeError(MUST_BE_OF_TYPE_PLURAL.format(i, f.__name__, type_name(at[1])))
                    else:
                        raise TypeError(MUST_BE_OF_TYPE_SINGULAR.format(i, f.__name__, type_name(at[1])))
                i += 1

            #verify named args
            for arg in kwarg_types:
                if arg in kwargs:
                    if not kwarg_types[arg] is not None and not isinstance(kwargs[arg], kwarg_types[arg]):
                        if len(arg) > 2:
                            raise TypeError(MUST_BE_OF_TYPE_PLURAL.format(arg, f.__name__, type_name(kwarg_types[arg])))
                        else:
                            raise TypeError(MUST_BE_OF_TYPE_SINGULAR.format(arg, f.__name__, type_name(kwarg_types[arg])))
            return f(*args, **kwargs)
        return inner_wrapper
    return outer_wrapper


def returns(return_type):
    def outer_wrapper(f):
        def inner_wrapper(*args, **kwargs):
            ret = f(*args, **kwargs)
            if not isinstance(ret, return_type):
                if len(return_type) > 2:
                    raise ReturnException(MUST_RETURN_TYPE_PLURAL.format(f.__name__, type_name(return_type)))
                else:
                    raise ReturnException(MUST_RETURN_TYPE_SINGULAR.format(f.__name__, type_name(return_type)))
            return ret
        return inner_wrapper
    return outer_wrapper