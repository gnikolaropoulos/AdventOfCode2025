def solve_part_1(puzzle_input):
    grid = [list(line) for line in puzzle_input]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    accessible_count = 0

    # Directions for 8 neighbors: up, down, left, right, and 4 diagonals
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "@":
                # Count adjacent rolls
                adjacent_rolls = 0
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if grid[ni][nj] == "@":
                            adjacent_rolls += 1

                # If fewer than 4 adjacent rolls, forklift can access it
                if adjacent_rolls < 4:
                    accessible_count += 1

    return accessible_count


def solve_part_2(puzzle_input):
    grid = [list(line) for line in puzzle_input]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Directions for 8 neighbors: up, down, left, right, and 4 diagonals
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    total_removed = 0

    while True:
        # Find all accessible rolls in this iteration
        accessible_positions = []

        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == "@":
                    # Count adjacent rolls
                    adjacent_rolls = 0
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < rows and 0 <= nj < cols:
                            if grid[ni][nj] == "@":
                                adjacent_rolls += 1

                    # If fewer than 4 adjacent rolls, forklift can access it
                    if adjacent_rolls < 4:
                        accessible_positions.append((i, j))

        # If no accessible rolls, we're done
        if not accessible_positions:
            break

        # Remove all accessible rolls
        for i, j in accessible_positions:
            grid[i][j] = "."

        total_removed += len(accessible_positions)

    return total_removed


def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(line.strip())
    return puzzle_input


if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
