def solve_part_1(puzzle_input):
    sum = 0
    for nums in puzzle_input:
        start = nums[0]
        end = nums[1]
        for i in range(start, end + 1):
            s = str(i)
            n = len(s)
            if n % 2 == 0:
                if s[: n // 2] == s[n // 2 :]:
                    sum += i
    return sum

def solve_part_2(puzzle_input):
    sum = 0
    for nums in puzzle_input:
        start = nums[0]
        end = nums[1]
        for i in range(start, end + 1):
            s = str(i)
            n = len(s)
            # Check if the string can be decomposed into a repeating pattern
            is_invalid = False
            for pattern_len in range(1, n // 2 + 1):
                if n % pattern_len == 0:
                    pattern = s[:pattern_len]
                    repetitions = n // pattern_len
                    if repetitions >= 2 and s == pattern * repetitions:
                        is_invalid = True
                        break
            if is_invalid:
                sum += i
    return sum

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        data = input_txt.read()
        puzzle_input = [tuple(map(int, part.split("-"))) for part in data.split(",")]
    return puzzle_input


if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
