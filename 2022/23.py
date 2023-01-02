from collections import defaultdict, deque

import aoc


def has_neighbor(r: int, c: int, elves: set[tuple[int, int]]):
    """Checks if any adjacent tile has an elf."""
    for j in range(-1, 2):
        for i in range(-1, 2):
            if j == 0 and i == 0: continue
            if (r+j, c+i) in elves:
                return True
    return False


def check_moves(r: int, c: int, moves: list[tuple[int, int]], elves: set[tuple[int, int]]):
    """Checks if elf can perform any move in the given moves list."""
    for dr, dc in moves:
        if (r+dr, c+dc) in elves:
            return False
    return True


def part1(lines: list[str]) -> int:
    elves = set([(r, c) for r, row in enumerate(lines) for c, v in enumerate(row) if v == '#'])

    # all possible directions
    directions = deque([
        ((-1, 0), [(-1,-1), (-1, 0), (-1, 1)]), # north
        (( 1, 0), [( 1,-1), ( 1, 0), ( 1, 1)]), # south
        (( 0,-1), [( 1,-1), ( 0,-1), (-1,-1)]), # west 
        (( 0, 1), [(-1, 1), ( 0, 1), ( 1, 1)]), # east
    ])

    rounds = 10
    for _ in range(rounds):
        # first half should consider all possible movements
        # dict keys = new positions and values = old positions
        candidates = defaultdict(list)
        for r, c in elves:
            if not has_neighbor(r, c, elves):
                # If no elves around me, I should stay put
                continue

            for (dr, dc), moves in directions:
                if check_moves(r, c, moves, elves):
                    # Looks like I can move in this direction
                    # Keep track of possible candidate to the new position
                    candidates[(r+dr, c+dc)].append((r, c))
                    break

        # second half should move the elves
        for new_pos, old_pos in candidates.items():
            if len(old_pos) == 1:
                # should move if there's only one candidate
                elves.remove(old_pos[0])
                elves.add(new_pos)

        # end of round
        directions.rotate(-1)

    # find boundaries to compute total number of tiles
    min_x, min_y = next(iter(elves))
    max_x, max_y = min_x, min_y
    for x, y in elves:
        if x < min_x: min_x = x
        if x > max_x: max_x = x
        if y < min_y: min_y = y
        if y > max_y: max_y = y

    total_tiles = (max_x - min_x + 1)*(max_y - min_y + 1)
    empty_tiles = total_tiles - len(elves)

    return empty_tiles


def part2(lines: list[str]) -> int:
    elves = set([(r, c) for r, row in enumerate(lines) for c, v in enumerate(row) if v == '#'])

    # all possible directions
    directions = deque([
        ((-1, 0), [(-1,-1), (-1, 0), (-1, 1)]), # north
        (( 1, 0), [( 1,-1), ( 1, 0), ( 1, 1)]), # south
        (( 0,-1), [( 1,-1), ( 0,-1), (-1,-1)]), # west 
        (( 0, 1), [(-1, 1), ( 0, 1), ( 1, 1)]), # east
    ])

    round = 0
    while True:
        round += 1
        # first half should consider all possible movements
        # dict keys = new positions and values = old positions
        candidates = defaultdict(list)
        for r, c in elves:
            if not has_neighbor(r, c, elves):
                # If no elves around me, I should stay put
                continue

            for (dr, dc), moves in directions:
                if check_moves(r, c, moves, elves):
                    # Looks like I can move in this direction
                    # Keep track of possible candidate to the new position
                    candidates[(r+dr, c+dc)].append((r, c))
                    break

        if not candidates:
            return round

        # second half should move the elves
        for new_pos, old_pos in candidates.items():
            if len(old_pos) == 1:
                # should move if there's only one candidate
                elves.remove(old_pos[0])
                elves.add(new_pos)

        # end of round
        directions.rotate(-1)

    # We will keep running until no elves can move
    return -1


if __name__ == '__main__':
    lines = aoc.load_input()
    print('part1', part1(lines))
    print('part2', part2(lines))
