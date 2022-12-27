#!/usr/bin/env python3

# 2, 1, 0, minus (written -), and double-minus (written =)
# minus = -1 and double-minus = -2
# For the snafu correction: 
#   3 is = because 3 - 5 = -2
#   4 is - because 4 - 5 = -1
_s2d = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
_d2s = {0: '0', 1: '1', 2: '2', 3: '=', 4: '-'}


def to_decimal(snafu: str) -> int:
    base = 1
    ans = 0
    for c in snafu[::-1]:
        ans += _s2d[c]*base
        base *= 5
    return ans


def to_snafu(dec: int) -> str:
    ans = ""
    while dec:
        # traditional base conversion using modular math
        dec, rem = divmod(dec, 5)
        ans = _d2s[rem] + ans
        # adjust traditional conversion: if negative output, use a "reverse" carry
        if rem > 3: dec += 1
    return ans


def solve(content: list[str]) -> str:
    return to_snafu(sum([to_decimal(line) for line in content]))


if __name__ == '__main__':
    # TODO: boilerplate code, move to common file
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        required=True,
                        default=None,
                        help='puzzle input filepath (e.g.: "input.txt" or "example.txt")')
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        content = f.read().splitlines()

    print(solve(content))
