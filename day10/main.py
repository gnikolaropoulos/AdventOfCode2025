import re
from typing import List, Tuple

# A machine is described by:
# (light_count, target_mask, button_list, joltage_targets)
# target_mask stores the desired on/off pattern for each light (bit set = on).
Machine = Tuple[int, int, List[List[int]], List[int]]

LINE_RE = re.compile(
    r"\[(?P<diagram>[.#]+)\]\s*(?P<buttons>(?:\([^)]*\)\s*)*)\{(?P<jolts>[^}]*)\}"
)


def popcount(x: int):
    # Use a portable popcount for environments without int.bit_count().
    return bin(x).count("1")


def parse_int_list(raw: str):
    raw = raw.strip()
    return [int(x.strip()) for x in raw.split(",") if x.strip()]


def parse_line(line: str):
    """
    Parse a single input line using regex to extract:
    - diagram inside [...]
    - zero or more button tuples (... )
    - joltage list inside {...}
    """
    m = LINE_RE.match(line)
    if not m:
        raise ValueError(f"Invalid machine description: {line}")

    diagram = m.group("diagram")
    num_lights = len(diagram)

    target_mask = 0
    for idx, ch in enumerate(diagram):
        if ch == "#":
            target_mask |= 1 << idx

    buttons = [
        parse_int_list(chunk)
        for chunk in re.findall(r"\(([^)]*)\)", m.group("buttons"))
    ]

    jolts = parse_int_list(m.group("jolts"))

    return num_lights, target_mask, buttons, jolts


def minimal_presses_for_machine(machine: Machine):
    num_lights, target_mask, buttons, _ = machine
    n_vars = len(buttons)

    # Build matrix rows for each light: row j has 1s where button toggles light j.
    rows: List[int] = []
    rhs: List[int] = []
    for light in range(num_lights):
        row_mask = 0
        for b_idx, toggle_list in enumerate(buttons):
            if light in toggle_list:
                row_mask |= 1 << b_idx
        rows.append(row_mask)
        rhs.append((target_mask >> light) & 1)

    # Gaussian elimination over GF(2) to reduced row-echelon form.
    pivot_cols: List[int] = []
    row = 0
    for col in range(n_vars):
        pivot = -1
        for r in range(row, num_lights):
            if (rows[r] >> col) & 1:
                pivot = r
                break
        if pivot == -1:
            continue

        rows[row], rows[pivot] = rows[pivot], rows[row]
        rhs[row], rhs[pivot] = rhs[pivot], rhs[row]

        for r in range(num_lights):
            if r != row and ((rows[r] >> col) & 1):
                rows[r] ^= rows[row]
                rhs[r] ^= rhs[row]

        pivot_cols.append(col)
        row += 1
        if row == num_lights:
            break

    free_cols = [c for c in range(n_vars) if c not in pivot_cols]
    free_mask = sum(1 << c for c in free_cols)

    pivot_rows = [
        (pivot_col, rows[r] & free_mask, rhs[r])
        for r, pivot_col in enumerate(pivot_cols)
    ]

    min_presses = None
    num_free = len(free_cols)

    # Enumerate all assignments to free variables; each yields one solution vector.
    for assignment in range(1 << num_free):
        x_mask = 0
        for bit_idx, col in enumerate(free_cols):
            if (assignment >> bit_idx) & 1:
                x_mask |= 1 << col

        for pivot_col, row_free_mask, b_val in pivot_rows:
            parity = popcount(row_free_mask & x_mask) & 1
            val = b_val ^ parity
            if val:
                x_mask |= 1 << pivot_col

        presses = popcount(x_mask)
        if min_presses is None or presses < min_presses:
            min_presses = presses

    # If there were no free variables and no pivot rows (no buttons), ensure target achievable.
    if min_presses is None:
        min_presses = 0

    return min_presses


def solve_part_1(puzzle_input: List[Machine]) -> int:
    return sum(minimal_presses_for_machine(machine) for machine in puzzle_input)


def minimal_presses_for_joltage(machine: Machine):
    _, _, buttons, jolts = machine

    m = len(jolts)
    n = len(buttons)

    if m == 0:
        return 0

    from fractions import Fraction

    # Build augmented matrix for rational Gaussian elimination.
    aug = []
    for row_idx in range(m):
        row = [Fraction(1 if row_idx in btn else 0) for btn in buttons]
        row.append(Fraction(jolts[row_idx]))
        aug.append(row)

    rank = 0
    pivot_cols: List[int] = []
    for col in range(n):
        pivot = None
        for r in range(rank, m):
            if aug[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue

        aug[rank], aug[pivot] = aug[pivot], aug[rank]

        factor = aug[rank][col]
        for c in range(col, n + 1):
            aug[rank][c] /= factor

        for r in range(m):
            if r != rank and aug[r][col] != 0:
                f = aug[r][col]
                for c in range(col, n + 1):
                    aug[r][c] -= f * aug[rank][c]

        pivot_cols.append(col)
        rank += 1

    free_cols = [c for c in range(n) if c not in pivot_cols]

    # If unique solution, just validate non-negative integers.
    if not free_cols:
        solution = [Fraction(0)] * n
        for r, pcol in enumerate(pivot_cols):
            solution[pcol] = aug[r][n]
        if any(val < 0 or val.denominator != 1 for val in solution):
            raise ValueError("No feasible non-negative integer solution.")
        return sum(int(val) for val in solution)

    # Express pivot variables as rhs - sum(coeff * free_var).
    expressions = []
    for r, pcol in enumerate(pivot_cols):
        coeffs = {}
        for fcol in free_cols:
            if aug[r][fcol] != 0:
                coeffs[fcol] = aug[r][fcol]
        expressions.append((aug[r][n], coeffs, pcol))

    # Simple, safe bounds for each free variable: a button cannot be pressed
    # more than the smallest target of the counters it affects.
    bounds = {}
    for fcol in free_cols:
        if buttons[fcol]:
            bounds[fcol] = (0, min(jolts[j] for j in buttons[fcol]))
        else:
            bounds[fcol] = (0, 0)

    best = None

    assign: List[int] = [0] * len(free_cols)

    def recurse(idx: int, partial_sum: int) -> None:
        nonlocal best
        if idx == len(free_cols):
            # Evaluate pivot variables.
            values = [0] * n
            free_map = {f: val for f, val in zip(free_cols, assign)}
            total = partial_sum
            for rhs, coeffs, pcol in expressions:
                val = rhs
                for fcol, coeff in coeffs.items():
                    val -= coeff * free_map[fcol]
                if val < 0 or val.denominator != 1:
                    return
                values[pcol] = int(val)
                total += int(val)
            # Free variables themselves.
            for fcol, val in free_map.items():
                values[fcol] = val
            if best is None or total < best:
                best = total
            return

        fcol = free_cols[idx]
        lo, hi = bounds[fcol]
        for val in range(lo, hi + 1):
            assign[idx] = val
            new_sum = partial_sum + val
            if best is None or new_sum < best:
                recurse(idx + 1, new_sum)
        assign[idx] = 0

    recurse(0, 0)

    return best


def solve_part_2(puzzle_input: List[Machine]) -> int:
    return sum(minimal_presses_for_joltage(machine) for machine in puzzle_input)


def get_puzzle_input(filename: str = "input.txt") -> List[Machine]:
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f]
    machines: List[Machine] = []
    for line in lines:
        if line.strip():
            machines.append(parse_line(line))
    return machines


if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
