def solve_part_1(puzzle_input):
    grid = puzzle_input
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])

    # Find start
    start_row = next(r for r, line in enumerate(grid) if "S" in line)
    start_col = grid[start_row].index("S")

    splits = 0
    visited = set()
    q = [(start_row + 1, start_col)]

    while q:
        r, c = q.pop()
        if r >= rows or c < 0 or c >= cols:
            continue
        if (r, c) in visited:
            continue
        visited.add((r, c))

        cell = grid[r][c]
        if cell == "^":
            splits += 1
            q.append((r + 1, c - 1))
            q.append((r + 1, c + 1))
        else:  # '.' or 'S'
            q.append((r + 1, c))

    return splits


def solve_part_2(puzzle_input):
    grid = puzzle_input
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    start_row = next(r for r, line in enumerate(grid) if "S" in line)
    start_col = grid[start_row].index("S")

    # ways[r][c] = number of timelines reaching (r, c)
    ways = [[0] * cols for _ in range(rows + 1)]
    exit_count = 0
    ways[start_row + 1][start_col] = 1

    for r in range(start_row + 1, rows):
        for c in range(cols):
            w = ways[r][c]
            if not w:
                continue
            cell = grid[r][c]
            if cell == "^":
                for nc in (c - 1, c + 1):
                    if 0 <= nc < cols:
                        ways[r + 1][nc] += w
                    else:
                        exit_count += w
            else:
                nr = r + 1
                if nr < rows:
                    ways[nr][c] += w
                else:
                    exit_count += w

    return exit_count


def get_puzzle_input():
    with open("input.txt") as f:
        return [line.rstrip("\n") for line in f]


if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
