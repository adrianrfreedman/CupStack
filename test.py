import unittest

import CupStack as cs

class TestCupStack(unittest.TestCase):
    def test_init(self):
        c = cs.CupStack()

        self.assertEqual(c._full,       0)
        self.assertEqual(c._capacity,   cs.CUP_VOLUME)

        self.assertIsNone(c._l)
        self.assertIsNone(c._r)

    def test_getters(self):
        c = cs.CupStack()

        self.assertEqual(c.full,        0)
        self.assertEqual(c.capacity,    cs.CUP_VOLUME)

        self.assertIsNone(c.l)
        self.assertIsNone(c.r)

    def test_fill(self):
        c = cs.CupStack()

        c.fill(0.1)
        self.assertEqual(c.full, 0.1)

        c.fill(0.2)
        self.assertEqual(c.full, c.capacity)

    def test_fill_with_decimal_precision(self):
        # In previous test the overflow avoids a well-known issue with floating
        # point precision in Python. I.e. 0.1 + 0.2 == 0.30000000000000004

        c = cs.CupStack(full=0.1, capacity=0.5)

        c.fill(0.2)
        self.assertEqual(c.full, 0.3)


if __name__ == '__main__':
    unittest.main()