import unittest
from unittest import mock

import CupStack as cs
import exercise

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

        self.assertRaises(cs.CupStackIndexError, lambda: c[0, 1])
        self.assertRaises(cs.CupStackIndexError, lambda: c[1, 0])
        self.assertRaises(cs.CupStackIndexError, lambda: c[4, 3])

        self.assertRaises(cs.CupStackIndexError, lambda: c[-1,  0])
        self.assertRaises(cs.CupStackIndexError, lambda: c[ 0, -1])
        
        self.assertRaises(cs.CupStackIndexError, lambda: c[[]])
        self.assertRaises(cs.CupStackIndexError, lambda: c[[0]])
        self.assertRaises(cs.CupStackIndexError, lambda: c[0, 1, 2])

    def test_08_index_type_errors(self):
        c = cs.CupStack()

        self.assertRaises(TypeError, lambda: c[0])
        self.assertRaises(TypeError, lambda: c['abc'])


    def test_09_index_on_stack(self):
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


    # Obviously not a unit test but good to see that output is expected
    def test_10_end_to_end_test(self):
        c = cs.CupStack(full=0, capacity=0.1, levels=4)

        c.fill(1)

        self.assertEqual(c[4, 0].full, 0)
        self.assertEqual(c[4, 1].full, 0.03125)
        self.assertEqual(c[4, 2].full, 0.0625)
        self.assertEqual(c[4, 3].full, 0.03125)
        self.assertEqual(c[4, 4].full, 0)

        c = cs.CupStack(full=0, capacity=0.25, levels=7)

        c.fill(7)

        self.assertEqual(c[7, 0].full, 0)
        self.assertEqual(c[7, 1].full, 0)
        self.assertEqual(c[7, 2].full, 0.16796875)
        self.assertEqual(c[7, 3].full, 0.25)
        self.assertEqual(c[7, 4].full, 0.25)
        self.assertEqual(c[7, 5].full, 0.16796875)
        self.assertEqual(c[7, 6].full, 0)
        self.assertEqual(c[7, 7].full, 0)


class TestExercise(unittest.TestCase):
    @mock.patch('exercise.cs.CupStack')
    @mock.patch('exercise.print')       # suppress output
    def test_11_correct_args(self, _, cs):
        exercise.main(3, 2, 1, 0)

        cs.assert_called_with(levels=3)
        cs.return_value.fill.assert_called_with(2)
        cs.return_value.__getitem__.assert_called_with((1, 0))

    @mock.patch('exercise.cs.CupStack')
    @mock.patch('exercise.sys')
    # @mock.patch('exercise.print')
    # def test_12_correct_args_with_error(self, _, sys, cs):
    def test_12_correct_args_with_error(self, sys, mock_cs):
        mock_cs.return_value.__getitem__.side_effect = cs.CupStackIndexError()

        exercise.main(3, 2, 5, 0)

        sys.exit.assert_called()


if __name__ == '__main__':
    unittest.main()