from __future__ import annotations

from collections import Counter, defaultdict, deque
from functools import lru_cache

with open("/Users/arash/Downloads/day20.txt") as f:
    puzzle = f.readlines()

# puzzle = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

# #..#.
# #....
# ##..#
# ..#..
# ..###""".split(
#     "\n"
# )

key = puzzle[0].strip()
points = set()
grid = []

for p in puzzle[1:]:
    if p == "\n" or p == "":
        continue
    v = p.strip()
    grid.append(v)

for r, row in enumerate(grid):
    for c, col in enumerate(row):
        if col == "#":
            points.add((r + 100, c + 100))


def get_neighbours(x, y):
    neighbours = []
    for a in range(-1, 2):
        for b in range(-1, 2):
            neighbours.append((x + a, y + b))
    return neighbours


def run_algorithm(key, points, r_min, r_max, c_min, c_max, default="0"):
    new_points = set()

    for x in range(r_min - 1, r_max + 2):
        for y in range(c_min - 1, c_max + 2):
            n = get_neighbours(x, y)
            idx_str = ""
            for r, c in n:
                if (r, c) in points:
                    idx_str += "1"
                elif r < r_min or r > r_max or c < c_min or c > c_max:
                    idx_str += default
                else:
                    idx_str += "0"

            idx = int(idx_str, 2)
            if key[idx] == "#":
                new_points.add((x, y))

    return new_points


minY = min([b for a, b in points])
minX = min([a for a, b in points])

maxY = max([b for a, b in points])
maxX = max([a for a, b in points])
default = "0"

for i in range(50):
    points = run_algorithm(key, points, minX, maxX, minY, maxY, default)
    minX -= 1
    maxX += 1
    minY -= 1
    maxY += 1
    if default == "0":
        default = "1"
    else:
        default = "0"
    if i == 1:
        print("part 1", len(points))

print("part 2", len(points))
