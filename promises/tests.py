import unittest
from promises import promise


class TestPromise(unittest.TestCase):
    @staticmethod
    @promise.accepts(promise.NUM, promise.NUM)
    @promise.returns(promise.NUM)
    def add_good(a, b):
        """
        Good adding function for testing `promise.accepts`.
        """
        return a + b

    @staticmethod
    @promise.accepts(promise.NUM, promise.NUM)
    @promise.returns(promise.NUM)
    def add_bad(a, b):
        """
        Bad adding function for testing `promise.returns`.
        """
        return 'LOL'

    def test_good_args_and_return(self):
        """
        Pass good args, expecting good output. Function is decorated with
        `promise.accepts` and `promise.returns`.
        """
        a, b = 1, 2
        self.assertEqual(self.add_good(a, b), a + b)

    def test_bad_args(self):
        """
        Pass bad args to a function decorated with promise.accepts.
        """
        with self.assertRaises(TypeError):
            _ = self.add_good('1', '2')

    def test_bad_return(self):
        with self.assertRaises(promise.ReturnException):
            _ = self.add_bad(1, 2)