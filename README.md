# Clean Code Bot

A Python project for clean code analysis and improvement.

## Setup

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. Create virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
clean-code-bot/
├── src/              # Source code
├── tests/            # Test files
├── requirements.txt  # Project dependencies
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

## Development

### CLI Usage

Clean Code Bot provides two main commands: `optimize` and `analyze`.

#### Optimize Command

Transform dirty or undocumented code into clean, optimized code:

```bash
python -m src.main optimize <input_file> [options]
```

**Options:**

- `--output, -o <file>`: Output file path (default: `<input>_optimized.py`)
- `--optimize <type>`: Optimization type: `all`, `solid`, `performance`, or `readability` (default: `all`)
- `--add-types`: Add type hints to functions and variables
- `--format`: Format code using black style
- `--verbose, -v`: Show detailed optimization report

**Example:**

```bash
python -m src.main optimize dirty_code.py --output clean_code.py --optimize all --add-types --verbose
```

#### Analyze Command

Analyze a Python file for code quality issues:

```bash
python -m src.main analyze <input_file> [options]
```

**Options:**

- `--verbose, -v`: Show detailed analysis report with suggestions

**Example:**

```bash
python -m src.main analyze my_code.py --verbose
```

### Running Tests

```bash
python -m pytest tests/
```

### Project Structure

```
clean-code-bot/
├── src/
│   ├── main.py           # CLI entry point
│   ├── cli.py            # CLI argument parser
│   ├── analyzer.py       # Code quality analysis
│   ├── optimizer.py      # Code optimization
│   ├── documenter.py     # Documentation generation
│   ├── utils.py          # Utility functions
│   └── __init__.py
├── tests/                # Test files
├── requirements.txt      # Project dependencies
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

### Features

- **Code Analysis**: Detects SOLID principle violations, missing documentation, and complexity issues
- **Code Optimization**: Applies readability improvements, naming conventions, and code refactoring
- **Documentation Generation**: Automatically adds comprehensive docstrings in Google style format
- **Type Hints**: Optional type annotation support
- **Code Formatting**: Black-style formatting for consistent code style

## License

MIT
