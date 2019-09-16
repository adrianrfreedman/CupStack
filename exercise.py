#!/usr/bin/python3.7
import argparse
import sys

import CupStack as cs


parser = argparse.ArgumentParser()
parser.add_argument(
    'levels',
    help='number of levels in the cup stack (zero-indexed)',
    type=int
)
parser.add_argument(
    'litres',
    help='number of litres to pour into the first cup',
    type=float
)
parser.add_argument(
    'i',
    help='row to inspect in the cup stack (zero-indexed)',
    type=int
)
parser.add_argument(
    'j',
    help='cup in the i-th row to inspect in the cup stack (zero-indexed)',
    type=int
)


def main(levels, litres, i, j):
    c = cs.CupStack(levels=levels)
    c.fill(litres)

    try:
        print(f'Cup i={i}, j={j} is {c[i, j].full} litres full')
    except cs.CupStackIndexError as e:
        sys.exit(e)
        

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.levels, args.litres, args.i, args.j)