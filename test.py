import unittest

import CupStack as cs

class TestCupStack(unittest.TestCase):
    def test_01_basic_init(self):
        c = cs.CupStack()

        self.assertEqual(c._full,       0)
        self.assertEqual(c._capacity,   cs.CUP_VOLUME)

        self.assertIsNone(c._l, c._r)

    def test_02_getters(self):
        c = cs.CupStack()

        self.assertEqual(c.full,        0)
        self.assertEqual(c.capacity,    cs.CUP_VOLUME)

        self.assertIsNone(c.l, c.r)

    def test_03_fill(self):
        c = cs.CupStack()

        c.fill(0.1)
        self.assertEqual(c.full, 0.1)

        c.fill(0.2)
        self.assertEqual(c.full, c.capacity)

    def test_04_fill_with_decimal_precision(self):
        # In previous test the overflow avoids a well-known issue with floating
        # point precision in Python. I.e. 0.1 + 0.2 == 0.30000000000000004

        c = cs.CupStack(full=0.1, capacity=0.5)

        c.fill(0.2)
        self.assertEqual(c.full, 0.3)

    def test_05_multi_level_init(self):
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

    def test_06_basic_index(self):
        c1 = cs.CupStack()

        # Check that a 0, 0 index on a level 0 stack returns the object itself
        c2 = c1[0, 0]
        self.assertEqual(id(c1), id(c2))

    def test_07_index_errors(self):
        c = cs.CupStack()

        self.assertRaises(IndexError, lambda: c[0, 1])
        self.assertRaises(IndexError, lambda: c[1, 0])
        self.assertRaises(IndexError, lambda: c[4, 3])

        self.assertRaises(IndexError, lambda: c[-1,  0])
        self.assertRaises(IndexError, lambda: c[ 0, -1])
        
        self.assertRaises(IndexError, lambda: c[[]])
        self.assertRaises(IndexError, lambda: c[[0]])
        self.assertRaises(IndexError, lambda: c[0, 1, 2])

    def test_08_index_type_errors(self):
        c = cs.CupStack()

        self.assertRaises(TypeError, lambda: c[0])
        self.assertRaises(TypeError, lambda: c['abc'])


    def test_08_index_on_stack(self):
        c = cs.CupStack(levels=1)
        
        self.assertEqual(id(c[1, 0]), id(c.l))
        self.assertEqual(id(c[1, 1]), id(c.r))

        l = 6
        c = cs.CupStack(levels=l)

        target = c
        for _ in range(l): target = target.l
        self.assertEqual(id(c[l, 0]), id(target))

        self.assertEqual(id(c[4, 2]), id(c.r.r.l.l))
        self.assertNotEqual(id(c[4, 2]), id(c.r.r.l.l.l))

    def test_09_overflow(self):
        c = cs.CupStack(levels=2)

        c.fill(0.25)
        self.assertEqual(c.full, c.capacity)

        cups = [c, c.l, c.r, c.l.r, c.r.l, c.l.l, c.r.r]
        for cup in cups[1:]:
            self.assertEqual(0, cup.full)

        c.fill(0.5)
        for cup in cups[:2]:
            self.assertEqual(cup.capacity, cup.full)

        for cup in cups[3:]:
           self.assertEqual(0, cup.full)

        c.fill(0.5)
        for cup in cups[:-3]:
            self.assertEqual(cup.capacity, cup.full)

        for cup in cups[-2:]:
           self.assertEqual(0.125, cup.full)


if __name__ == '__main__':
    unittest.main()