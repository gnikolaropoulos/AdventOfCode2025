from typing import List, Tuple

Point = Tuple[int, int]


def solve_part_1(puzzle_input: List[Point]):
    max_area = 0
    n = len(puzzle_input)

    for i in range(n):
        x1, y1 = puzzle_input[i]
        for j in range(i + 1, n):
            x2, y2 = puzzle_input[j]
            # Include both corner tiles, so add 1 to each dimension
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area > max_area:
                max_area = area

    return max_area


def solve_part_2(puzzle_input):
    # Build polygon edges (points are ordered and wrap).
    points = puzzle_input
    n = len(points)

    vertical_edges = []  # (x, y1, y2) with y1 < y2
    horizontal_by_y = {}

    for i in range(n):
        (x1, y1) = points[i]
        (x2, y2) = points[(i + 1) % n]
        if x1 == x2:
            if y1 < y2:
                vertical_edges.append((x1, y1, y2))
            else:
                vertical_edges.append((x1, y2, y1))
        else:
            y = y1
            a, b = (x1, x2) if x1 < x2 else (x2, x1)
            horizontal_by_y.setdefault(y, []).append((a, b))

    ys = sorted({y for _, y in points})

    def merge_intervals(intervals: List[Tuple[int, int]]):
        if not intervals:
            return []
        intervals.sort()
        merged = [intervals[0]]
        for l, r in intervals[1:]:
            ml, mr = merged[-1]
            if l <= mr + 1:
                merged[-1] = (ml, max(mr, r))
            else:
                merged.append((l, r))
        return merged

    def intervals_cover(intervals: List[Tuple[int, int]], l: int, r: int):
        for a, b in intervals:
            if a <= l and b >= r:
                return True
        return False

    def compute_intervals_for_row(y: int, include_horizontal: bool):
        crossings = []
        for x, y1, y2 in vertical_edges:
            if y >= y1 and y < y2:
                crossings.append(x)
        crossings.sort()

        intervals: List[Tuple[int, int]] = []
        for i in range(0, len(crossings), 2):
            if i + 1 < len(crossings):
                intervals.append((crossings[i], crossings[i + 1]))

        if include_horizontal and y in horizontal_by_y:
            intervals.extend(horizontal_by_y[y])

        return merge_intervals(intervals)

    vertex_row_intervals = {y: compute_intervals_for_row(y, True) for y in ys}

    bands = []
    for a, b in zip(ys, ys[1:]):
        if b - a <= 1:
            continue
        sample_y = a + 1
        intervals = compute_intervals_for_row(sample_y, False)
        bands.append((a + 1, b - 1, intervals))

    # Evaluate all rectangles defined by pairs of red points
    max_area = 0
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            xmin, xmax = (x1, x2) if x1 <= x2 else (x2, x1)
            ymin, ymax = (y1, y2) if y1 <= y2 else (y2, y1)

            valid = True

            # Check vertex rows within the rectangle
            for y in ys:
                if ymin <= y <= ymax:
                    if not intervals_cover(vertex_row_intervals[y], xmin, xmax):
                        valid = False
                        break
            if not valid:
                continue

            # Check bands (rows strictly between vertex rows)
            for start, end, intervals in bands:
                if end < ymin or start > ymax:
                    continue
                if not intervals_cover(intervals, xmin, xmax):
                    valid = False
                    break

            if valid:
                area = (xmax - xmin + 1) * (ymax - ymin + 1)
                if area > max_area:
                    max_area = area

    return max_area


def get_puzzle_input():
    lines = []
    with open("input.txt") as f:
        lines = [line.rstrip("\n") for line in f]
    tiles: List[Point] = []
    for line in lines:
        parts = line.strip().split(",")
        x, y = map(int, parts[:2])
        tiles.append((x, y))
    return tiles


if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
