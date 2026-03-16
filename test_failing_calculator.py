import unittest

from failing_calculator import average_ratios


class TestAverageRatios(unittest.TestCase):
    def test_with_zero(self):
        # [10,5,0] -> ratios = [100/10, 100/5] = [10, 20] -> avg = 15
        self.assertAlmostEqual(average_ratios([10, 5, 0]), 15.0)

    def test_all_zero(self):
        with self.assertRaises(ValueError):
            average_ratios([0, 0])

    def test_invalid_iterable(self):
        with self.assertRaises(TypeError):
            average_ratios(123)  # not iterable

    def test_non_numeric_item(self):
        with self.assertRaises(TypeError):
            average_ratios([10, "a"])


if __name__ == "__main__":
    unittest.main()
