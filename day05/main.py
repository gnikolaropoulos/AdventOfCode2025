def solve_part_1(puzzle_input):
    # Find the blank line that separates ranges from IDs
    blank_line_idx = -1
    for i, line in enumerate(puzzle_input):
        if not line.strip():  # Found blank line
            blank_line_idx = i
            break

    # Parse ranges
    ranges = []
    for line in puzzle_input[:blank_line_idx]:
        if line.strip() and "-" in line:
            start, end = map(int, line.split("-"))
            ranges.append((start, end))

    # Parse ingredient IDs
    ingredient_ids = []
    start_idx = blank_line_idx + 1 if blank_line_idx >= 0 else blank_line_idx
    for line in puzzle_input[start_idx:]:
        if line.strip():  # Skip empty lines
            ingredient_ids.append(int(line.strip()))

    # Count how many ingredient IDs are fresh (fall into any range)
    fresh_count = 0
    for ingredient_id in ingredient_ids:
        is_fresh = False
        for start, end in ranges:
            if start <= ingredient_id <= end:
                is_fresh = True
                break
        if is_fresh:
            fresh_count += 1

    return fresh_count


def solve_part_2(puzzle_input):
    # Find the blank line that separates ranges from IDs
    blank_line_idx = -1
    for i, line in enumerate(puzzle_input):
        if not line.strip():  # Found blank line
            blank_line_idx = i
            break

    # Parse ranges
    ranges = []
    for line in puzzle_input[:blank_line_idx]:
        if line.strip() and "-" in line:
            start, end = map(int, line.split("-"))
            ranges.append((start, end))

    # Optimize: Merge overlapping ranges and count total coverage
    # Sort ranges by start value
    ranges.sort(key=lambda x: x[0])

    # Merge overlapping/adjacent ranges
    merged = []
    for start, end in ranges:
        if not merged:
            merged.append((start, end))
        else:
            last_start, last_end = merged[-1]
            # If current range overlaps or is adjacent to the last merged range
            if start <= last_end + 1:
                # Merge: extend the last range if needed
                merged[-1] = (last_start, max(last_end, end))
            else:
                # No overlap, add as new range
                merged.append((start, end))

    # Count total unique IDs covered by merged ranges
    total_fresh = 0
    for start, end in merged:
        total_fresh += end - start + 1  # Inclusive range

    return total_fresh


def get_puzzle_input():
    with open("input.txt") as input_txt:
        content = input_txt.read()
    # Split by newlines, preserving empty lines
    puzzle_input = content.split("\n")
    # Remove trailing empty line if file ends with newline
    if puzzle_input and not puzzle_input[-1]:
        puzzle_input.pop()
    return puzzle_input


if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
