import unittest
from op_evalv2 import EvalExp


class TestStringMethods(unittest.TestCase):

    def test(self):
        res = EvalExp('1 + 2 * 3 - 4').eval()
        self.assertEqual(res, 3)
        res = EvalExp('-1 + 2 * 3 - 4').eval()
        self.assertEqual(res, 1)
        res = EvalExp('1 + 2 * (3 + 3) / 2').eval()
        self.assertEqual(res, 7)
        res = EvalExp('(1 + 2 * (3 + 3) / 2)/2').eval()
        self.assertEqual(res, 3.5)

if __name__ == '__main__':
    unittest.main()
