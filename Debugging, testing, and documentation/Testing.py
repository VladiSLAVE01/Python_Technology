import unittest
import math


class TestDivide(unittest.TestCase):

    def test_both_negative_number(self):
        self.assertEqual(divide(-10, -2), 5)
        self.assertEqual(divide(10, -2), -5)
        self.assertEqual(divide(-10, 2), -5)
        self.assertEqual(divide(math.pi, math.pi), 1)

    def test_float_dividend_integer_divisor(self):
        self.assertEqual(divide(15.0, 3), 5.0)
        self.assertEqual(divide(0.01, 0.02), 0.5)
        self.assertEqual(divide(0.10, -0.05), -2)
        self.assertEqual(divide(-10, 0.5), -20.0)

    def test_result_very_small_positive_float(self):
        self.assertEqual(divide(1, 1_000_000_000_000), 1e-12)
        self.assertEqual(divide(1000000, 200), 5000)
        self.assertEqual(divide(0, 5), 0)

    def test_divide_by_zero(self):
        self.assertEqual(divide(10, 0), "Can't divide by zero")
        self.assertEqual(divide(-5, 0), "Can't divide by zero")
        self.assertEqual(divide(0, 0), "Can't divide by zero")
        self.assertEqual(divide(0.5, 0), "Can't divide by zero")

    def test_large_numbers(self):
        self.assertEqual(divide(1_000_000, 1_000), 1_000)
        self.assertEqual(divide(10 ** 12, 10 ** 6), 10 ** 6)
        self.assertEqual(divide(-1_000_000, 1_000), -1_000)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDivide)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
