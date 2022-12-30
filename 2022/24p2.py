import input
from collections import defaultdict, deque
from heapq import heappop, heappush


def explore(sy, sx, gy, gx, max_y, max_x, blizzards):
    space = []
    possible_moves = [(0,1), (0,-1), (1,0), (-1,0), (0,0)]
    visited = set()
    period = len(blizzards)

    # we shall explore first the positions that consumed less time to be visited
    heappush(space, ((0, (sy, sx))))
    while space:
        minute, (oy, ox) = heappop(space)

        mmod = minute % period
        if (oy, ox, mmod) in visited:
            continue
        visited.add((oy, ox, mmod))

        minute += 1
        local_bliz = blizzards[minute % period]
        for dy, dx in possible_moves:
            ny, nx = oy+dy, ox+dx
            if (ny, nx) in local_bliz: 
                # blizzard! cannot go there!
                continue
            
            if ny == gy and nx == gx:
                return minute

            if not (nx == ox and ny == oy) and (nx <= 0 or nx >= max_x or ny <= 0 or ny >= max_y):
                # out of bounds
                continue

            heappush(space, (minute, (ny, nx)))
        
    return -1


def wrap_around(value, max_value):
    """0 and max_value are out of bounds, so we need to wrap around"""
    if value == 0: return max_value-1
    if value == max_value: return 1
    return value


def update_blizzard(bliz, max_y, max_x):
    new_bliz = defaultdict(list)
    for (oy, ox), moves in bliz.items():
        for dy, dx in moves:
            ny = wrap_around(oy+dy, max_y)
            nx = wrap_around(ox+dx, max_x)
            new_bliz[ny, nx].append((dy, dx))             
    
    return new_bliz


def forecast_blizzards(grid: list[str], max_y, max_x) -> list:
    # load initial state
    moves = { '>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0) }
    bliz = defaultdict(list)
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value in moves:
                bliz[y, x].append(moves[value])
    
    # forecast means update state until repeat
    initial_state = bliz.keys()
    forecast = []
    while True:
        forecast.append(bliz.keys())
        bliz = update_blizzard(bliz, max_y, max_x)
        if bliz.keys() == initial_state:
            break

    return forecast


def solve(grid: list[str]) -> int:
    max_y, max_x = len(grid)-1, len(grid[0])-1
    print('0. forecast blizzards...', max_y, max_x)
    blizzards = deque(forecast_blizzards(grid, max_y, max_x))
    
    sy, sx = 0, 1
    gy, gx = max_y, max_x-1
    total = 0
    print(f'1. explore from {sy, sx} to {gy, gx} start time {total}...')
    minute = explore(sy, sx, gy, gx, max_y, max_x, blizzards)
    blizzards.rotate(-minute)
    total += minute
    print(f'2. explore from {gy, gx} to {sy, sx} start time {total}...')
    minute = explore(gy, gx, sy, sx, max_y, max_x, blizzards)
    blizzards.rotate(-minute)
    total += minute
    print(f'3. explore from {sy, sx} to {gy, gx} start time {total}...')
    minute = explore(sy, sx, gy, gx, max_y, max_x, blizzards)
    total += minute
    print(f'4. finished at minute {total}')
    
    return total


if __name__ == '__main__':
    print(solve(input.readlines()))
