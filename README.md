# AdventOfCode2025
AoC 2025's Python solutions

## Requirements
- Python 3.10 or higher (recommended: Python 3.11+)
- No external dependencies required

## Project Structure
Each day's solution is self-contained in its own directory:
```
day01/
├── day01.py      # Solution code
└── input.txt     # Puzzle input
```

## Running Solutions
Navigate to any day's directory and run the Python script:
```bash
cd day01
python day01.py
```

Or run from the project root:
```bash
python day01/day01.py
```

## Development Setup (Optional)
This project has zero runtime dependencies. However, for code quality tools during development:

```bash
# Install optional development tools
pip install -e ".[dev]"

# Or manually:
pip install black ruff mypy
```

### Development Tools
- **black**: Code formatter for consistent style
- **ruff**: Fast linter for code quality checks
- **mypy**: Static type checker (some solutions use type hints)

### Running Code Quality Checks
```bash
# Format code
black .

# Lint code
ruff check .

# Type check (for files with type hints)
mypy day*/*.py
```

## Dependencies
This project intentionally uses **zero external dependencies**, relying only on Python's standard library:
- `typing` - Type hints
- `heapq` - Heap queue algorithms
- `re` - Regular expressions

See `DEPENDENCY_AUDIT.md` for a complete dependency analysis and security audit. 
