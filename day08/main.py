import heapq
from typing import List, Tuple

Point = Tuple[int, int, int]


def k_closest_pairs(points: List[Point], k: int) -> List[Tuple[int, int, int]]:
    n = len(points)

    heap: List[Tuple[int, int, int]] = []  # stores (-dist2, i, j)

    for i in range(n):
        x1, y1, z1 = points[i]
        for j in range(i + 1, n):
            x2, y2, z2 = points[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist = dx * dx + dy * dy + dz * dz

            if len(heap) < k:
                heapq.heappush(heap, (-dist, i, j))
            elif dist < -heap[0][0]:
                heapq.heapreplace(heap, (-dist, i, j))

    # Convert back to positive distances and sort ascending
    closest = [(-neg_dist, i, j) for neg_dist, i, j in heap]
    closest.sort(key=lambda x: x[0])
    return closest


def solve_part_1(puzzle_input):
    n = len(puzzle_input)

    # Take only the 1000 closest edges to match puzzle constraint.
    pairs = k_closest_pairs(puzzle_input, 1000)

    parent = list(range(n))
    size = [1] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    for _, i, j in pairs:
        union(i, j)

    largest = sorted(size, reverse=True)

    return largest[0] * largest[1] * largest[2]


def solve_part_2(puzzle_input):
    n = len(puzzle_input)

    edges: List[Tuple[int, int, int]] = []
    for i in range(n):
        x1, y1, z1 = puzzle_input[i]
        for j in range(i + 1, n):
            x2, y2, z2 = puzzle_input[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist = dx * dx + dy * dy + dz * dz
            edges.append((dist, i, j))

    edges.sort(key=lambda e: e[0])

    parent = list(range(n))
    size = [1] * n
    components = n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> bool:
        nonlocal components
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        components -= 1
        return True

    last_i = last_j = -1
    for _, i, j in edges:
        if union(i, j):
            last_i, last_j = i, j
            if components == 1:
                break

    return puzzle_input[last_i][0] * puzzle_input[last_j][0]


def get_puzzle_input():
    lines = []
    with open("input.txt") as f:
        lines = [line.rstrip("\n") for line in f]
    points = []
    for line in lines:
        if not line.strip():
            continue
        x, y, z = map(int, line.split(","))
        points.append((x, y, z))
    return points


if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
