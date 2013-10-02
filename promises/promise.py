from collections import Container

ARGUMENT_IS_REQUIRED = "The named argument `{}` is required"

MUST_RETURN_TYPE_SINGULAR = "Function must return type {}"
MUST_RETURN_TYPE_PLURAL = "Function must return one of these types: {}"
MUST_BE_OF_TYPE_SINGULAR = "Argument {} must be of type {}"
MUST_BE_OF_TYPE_PLURAL =  "Argument {} must be one of these types: {}"


INT = int, long,
DEC = float,
NUM = INT + DEC + (complex,)
TEXT = str, unicode,
SEQ = str, unicode, list, tuple, bytearray, buffer, xrange,
SET = set, frozenset,
MAP = dict,
ITER = SEQ + SET + MAP,


class ReturnException(Exception):
    """
    Raised when a function returns a value of the wrong type.
    """
    pass


class RequiredError(Exception):
    """
    Raised when a required named argument is not passed.
    """
    pass


def type_name(t):
    if isinstance(t, ITER):
        return reduce(lambda x, y: x + ", " + y, map(lambda x: x.__name__, t))
    else:
        return t.__name__


def require(*args):
    """
    Decorator to require a named argument. Used to force named argument usage when type enforcement is desired.
    """
    def outer_wrapper(f):
        def inner_wrapper(*f_args, **f_kwargs):
            for arg in args:
                if arg not in f_kwargs:
                    raise RequiredError(ARGUMENT_IS_REQUIRED.format(arg))
            return f(*f_args, **f_kwargs)
        return inner_wrapper
    return outer_wrapper


def accepts(*arg_types, **kwarg_types):
    """
    Decorator to add argument type checking to functions.

    Takes positional and named arguments.
    """
    def outer_wrapper(f):
        def inner_wrapper(*args, **kwargs):
            #verify positional args
            args_n_types = zip(args, arg_types)
            i = 0
            for at in args_n_types:
                if at[1] is not None and not isinstance(at[0], at[1]):
                    if isinstance(at[1], ()):
                        raise TypeError(MUST_BE_OF_TYPE_PLURAL.format(i, type_name(at[1])))
                    else:
                        raise TypeError(MUST_BE_OF_TYPE_SINGULAR.format(i, type_name(at[1])))
                i += 1

            #verify named args
            for arg in kwarg_types:
                if arg in kwargs:
                    if not kwarg_types[arg] is not None and not isinstance(kwargs[arg], kwarg_types[arg]):
                        if isinstance(kwarg_types[arg], Container) and len(arg) > 2:
                            raise TypeError(MUST_BE_OF_TYPE_PLURAL.format(arg, type_name(kwarg_types[arg])))
                        else:
                            raise TypeError(MUST_BE_OF_TYPE_SINGULAR.format(arg, type_name(kwarg_types[arg])))
            return f(*args, **kwargs)
        return inner_wrapper
    return outer_wrapper


def returns(return_type):
    """
    Decorator to add return value type checking to functions.
    """
    def outer_wrapper(f):
        def inner_wrapper(*args, **kwargs):
            ret = f(*args, **kwargs)
            if not isinstance(ret, return_type):
                if isinstance(return_type, Container) and len(return_type) > 2:
                    raise ReturnException(MUST_RETURN_TYPE_PLURAL.format(type_name(return_type)))
                else:
                    raise ReturnException(MUST_RETURN_TYPE_SINGULAR.format(type_name(return_type)))
            return ret
        return inner_wrapper
    return outer_wrapper
