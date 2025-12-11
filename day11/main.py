from typing import Dict, List

Graph = Dict[str, List[str]]


def parse_line(line: str):
    head, tail = line.split(":")
    node = head.strip()
    targets = tail.strip().split()
    return node, targets


def count_paths(graph: Graph, start: str, goal: str):
    memo: Dict[str, int] = {}
    visiting = set()

    def dfs(node: str) -> int:
        if node == goal:
            return 1
        if node in memo:
            return memo[node]
        visiting.add(node)
        total = 0
        for nxt in graph.get(node):
            total += dfs(nxt)
        visiting.remove(node)
        memo[node] = total
        return total

    return dfs(start)


def count_paths_through(graph: Graph, start: str, goal: str, required: List[str]):
    required_set = frozenset(required)
    memo: Dict[tuple, int] = {}
    visiting = set()

    def dfs(node: str, remaining: frozenset):
        next_remaining = remaining - {node} if node in remaining else remaining
        if node == goal:
            return 1 if not next_remaining else 0

        key = (node, next_remaining)
        if key in memo:
            return memo[key]
        visiting.add(key)

        total = 0
        for nxt in graph.get(node, []):
            total += dfs(nxt, next_remaining)

        visiting.remove(key)
        memo[key] = total
        return total

    return dfs(start, required_set)


def solve_part_1(puzzle_input: Graph):
    return count_paths(puzzle_input, "you", "out")


def solve_part_2(puzzle_input):
    return count_paths_through(puzzle_input, "svr", "out", ["dac", "fft"])


def get_puzzle_input(filename: str = "input.txt"):
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f]
    graph: Graph = {}
    for line in lines:
        if not line.strip():
            continue
        node, targets = parse_line(line)
        graph[node] = targets
    return graph


if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
