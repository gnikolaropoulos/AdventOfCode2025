def solve_part_1(puzzle_input):
    total_joltage = 0
    
    for bank in puzzle_input:
        max_joltage = 0
        # Find all pairs of indices (i, j) where i < j
        for i in range(len(bank)):
            for j in range(i + 1, len(bank)):
                # Form the two-digit number from digits at positions i and j
                joltage = int(bank[i] + bank[j])
                max_joltage = max(max_joltage, joltage)
        total_joltage += max_joltage
    
    return total_joltage

def solve_part_2(puzzle_input):
    total_joltage = 0
    
    for bank in puzzle_input:
        n = len(bank)
        k = 12  # Need to select exactly 12 batteries
        
        # Use greedy approach: for each of the 12 positions,
        # select the maximum digit available while ensuring we can
        # still select enough digits to complete the 12
        selected_indices = []
        start_idx = 0
        
        for pos in range(k):
            # For position 'pos', we can choose from indices [start_idx, n - (k - pos)]
            # This ensures we have enough digits left to complete the selection
            end_idx = n - (k - pos) + 1
            max_digit = -1
            max_idx = -1
            
            # Find the maximum digit in the available range
            for i in range(start_idx, end_idx):
                digit = int(bank[i])
                if digit > max_digit:
                    max_digit = digit
                    max_idx = i
            
            selected_indices.append(max_idx)
            start_idx = max_idx + 1
        
        # Form the number from selected digits
        joltage_str = ''.join(bank[i] for i in selected_indices)
        joltage = int(joltage_str)
        total_joltage += joltage
    
    return total_joltage

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
