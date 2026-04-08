# Clean Code Bot Examples

This folder contains before-and-after examples showing how Clean Code Bot transforms code.

## Files

### `before_example.py`

Demonstrates common code quality issues:

- **Multiple responsibilities** in single functions
- **Poor naming** and structure
- **Missing documentation** (docstrings)
- **Security vulnerabilities** (SQL injection)
- **Tight coupling** between operations
- **No type hints**

### `after_example.py`

Shows the cleaned, optimized version:

- **Single Responsibility Principle** - each function has one job
- **Clear naming** and logical structure
- **Comprehensive docstrings** in Google style format
- **Secure practices** - parameterized queries
- **Loose coupling** - reusable components
- **Full type hints** for static analysis
- **Input validation** and error handling

## Key Improvements

### 1. Separation of Concerns

**Before:**

```python
def process_user_data(data):
    users = []
    for d in data:
        if d['age'] >= 18:  # Filtering logic
            name = d['name'].strip().title()  # Formatting logic
            email = d['email'].lower()
            score = (d['age'] - 18) * 0.5 + len(d['name']) * 0.1  # Calculation logic
            users.append({'name': name, 'email': email, 'score': score})
    return users
```

**After:**

```python
# Each concern is a separate function
adults = filter_adult_users(data)
normalized = normalize_user_names(adults)
processed = process_user_data(data)  # Orchestrates the pipeline
```

### 2. Documentation

**Before:** No docstrings

**After:** Comprehensive Google-style docstrings with:

- Description of purpose
- Args with types
- Returns with types
- Raises for exceptions
- Examples showing usage

### 3. Security

**Before:** SQL Injection vulnerability

```python
query = f"INSERT INTO users VALUES({user_id},'{info}')"  # Danger!
```

**After:** Safe parameterized query

```python
query = "INSERT INTO users (id, info) VALUES (?, ?)"
cursor.execute(query, (user_id, user_info))  # Safe
```

### 4. Type Safety

**Before:** No type hints

**After:** Full type annotations

```python
def process_user_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
```

## Usage

Use Clean Code Bot to analyze and improve these examples:

```bash
# Analyze the dirty code
python -m src.main analyze before_example.py --verbose

# Optimize with AI assistance (requires LLM API key)
python -m src.main improve before_example.py --ai --provider groq
```

## See Also

- [Main README](../README.md)
- [CLI Documentation](../README.md#cli-usage)
