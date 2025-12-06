def find_separators(lines):
    max_width = max(len(line) for line in lines)
    seps = [
        col
        for col in range(max_width)
        if all(col >= len(line) or line[col] == " " for line in lines)
    ]
    return seps, max_width


def slices_from_separators(seps, max_width):
    slices, start = [], 0
    for sep in seps:
        if start < sep:
            slices.append((start, sep))
        start = sep + 1
    if start < max_width:
        slices.append((start, max_width))
    return slices


def apply(numbers, op):
    if op == "+":
        return sum(numbers)
    result = 1
    for n in numbers:
        result *= n
    return result


def solve_part_1(puzzle_input):
    seps, max_width = find_separators(puzzle_input)
    slices = slices_from_separators(seps, max_width)

    total = 0
    for start, end in slices:
        col_data = [
            seg for line in puzzle_input if (seg := line[start:end].strip())
        ]
        if len(col_data) < 2:
            continue
        op, nums = col_data[-1].strip(), []
        for val in col_data[:-1]:
            nums.append(int(val))

        total += apply(nums, op)
    return total


def solve_part_2(puzzle_input):
    seps, max_width = find_separators(puzzle_input)
    slices = slices_from_separators(seps, max_width)

    total = 0
    for start, end in slices:
        width = end - start
        if width <= 0:
            continue

        nums, op = [], None
        for rel_col in range(width - 1, -1, -1):
            abs_col = start + rel_col
            col = [line[abs_col] if abs_col < len(line) else " " for line in puzzle_input]
            if col[-1] in "+*":
                op = col[-1]
            digits = "".join(ch for ch in col[:-1] if ch != " ")
            if digits:
                nums.append(int(digits))

        total += apply(nums, op)

    return total


def get_puzzle_input():
    with open("input.txt") as input_txt:
        return input_txt.read().splitlines()


if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
