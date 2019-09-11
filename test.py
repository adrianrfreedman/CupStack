import unittest

import CupStack as cs

class TestCupStack(unittest.TestCase):
    def test_basic_init(self):
        c = cs.CupStack()

        self.assertEqual(c._full,       0)
        self.assertEqual(c._capacity,   cs.CUP_VOLUME)

        self.assertIsNone(c._l, c._r)

    def test_getters(self):
        c = cs.CupStack()

        self.assertEqual(c.full,        0)
        self.assertEqual(c.capacity,    cs.CUP_VOLUME)

        self.assertIsNone(c.l, c.r)

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

    def test_multi_level_init(self):
        c = cs.CupStack(full=12, capacity=13, levels=4)

        stack = [c]
        visited = set()
        while stack:
            curr = stack.pop()

            # If at a cup on the bottom row make some checks
            if curr.l is None and curr.r is None:
                self.assertIsInstance(curr, cs.CupStack)
                self.assertEqual(c.full, curr.full)
                self.assertEqual(c.capacity, curr.capacity)


            if curr.l is not None and curr.l not in visited:
                stack.append(curr.l)

            if curr.r is not None:
                if curr.r not in visited:
                    stack.append(curr.r)
                
                # If 2 rows from the bottom, check for shared cups
                # I.e. check that the left child's right child is the same
                # object as the right child's left child
                #   o      o
                #  l   ==   r
                # . x      x .
                if curr.r.r is not None:
                    self.assertEqual(id(curr.l.r), id(curr.r.l))

            visited.add(curr)


if __name__ == '__main__':
    unittest.main()