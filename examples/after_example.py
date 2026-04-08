"""
Cleaned and optimized version of the before_example.py file.

This module demonstrates proper code structure, documentation, and security practices.
"""

from typing import List, Dict, Any
import sqlite3


def filter_adult_users(users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter users who are 18 years or older (adults).

    Args:
        users: List of user dictionaries with 'age' key.

    Returns:
        List[Dict]: Filtered list containing only users aged 18+.

    Example:
        >>> users = [{'name': 'John', 'age': 20}, {'name': 'Jane', 'age': 16}]
        >>> adults = filter_adult_users(users)
        >>> len(adults)
        1
    """
    return [user for user in users if user.get("age", 0) >= 18]


def normalize_user_names(users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normalize user names and emails to consistent format.

    Operations:
        - Strip whitespace from names
        - Convert names to title case
        - Convert emails to lowercase

    Args:
        users: List of user dictionaries with 'name' and 'email' keys.

    Returns:
        List[Dict]: Users with normalized name and email fields.
    """
    normalized = []
    for user in users:
        user_copy = user.copy()
        user_copy["name"] = user.get("name", "").strip().title()
        user_copy["email"] = user.get("email", "").lower()
        normalized.append(user_copy)
    return normalized


def calculate_user_score(age: int, name_length: int, max_score: int = 50) -> float:
    """
    Calculate user engagement/trust score.

    Scoring formula:
        - Base: (age - 18) * 0.5 points
        - Bonus: name_length * 0.1 points
        - Maximum: capped at max_score

    Args:
        age: User age in years.
        name_length: Length of user's name.
        max_score: Maximum score cap (default: 50).

    Returns:
        float: Calculated score between 0 and max_score.

    Raises:
        ValueError: If age is negative or name_length is negative.
    """
    if age < 0:
        raise ValueError("Age cannot be negative")
    if name_length < 0:
        raise ValueError("Name length cannot be negative")

    score = (age - 18) * 0.5 + name_length * 0.1
    return min(score, max_score)


def process_user_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process and enrich user data with normalized format and scores.

    Single Responsibility:
        - Separates filtering, normalization, and scoring logic
        - Each step is independently testable

    Args:
        data: List of raw user dictionaries.

    Returns:
        List[Dict]: Processed users with name, email, and score fields.

    Raises:
        ValueError: If data contains invalid entries.
    """
    if not data:
        return []

    # Step 1: Filter adults only
    adults = filter_adult_users(data)

    # Step 2: Normalize names and emails
    normalized = normalize_user_names(adults)

    # Step 3: Enrich with scores
    processed = []
    for user in normalized:
        age = user.get("age", 0)
        name_len = len(user.get("name", ""))

        try:
            score = calculate_user_score(age, name_len)
            user_data = {
                "name": user["name"],
                "email": user["email"],
                "score": score,
            }
            processed.append(user_data)
        except ValueError as e:
            raise ValueError(f"Error processing user {user.get('name')}: {e}")

    return processed


class UserDataProcessor:
    """
    Processes and manages user data with clear responsibilities.

    Follows Single Responsibility Principle:
        - Data input and storage
        - Filtering operations
        - Processing pipeline

    Attributes:
        _raw_data: Raw input data storage.
        _filtered_data: Filtered data after validation.
        _processed_data: Final processed data.
    """

    def __init__(self) -> None:
        """Initialize the user data processor with empty data storage."""
        self._raw_data: List[Dict[str, Any]] = []
        self._filtered_data: List[Dict[str, Any]] = []
        self._processed_data: List[Dict[str, Any]] = []

    def add_user(self, user_data: Dict[str, Any]) -> None:
        """
        Add a single user record to the processor.

        Args:
            user_data: User record dictionary.

        Raises:
            TypeError: If user_data is not a dictionary.
        """
        if not isinstance(user_data, dict):
            raise TypeError("User data must be a dictionary")
        self._raw_data.append(user_data)

    def filter_adults(self) -> None:
        """Filter raw data to include only adult users (age >= 18)."""
        self._filtered_data = filter_adult_users(self._raw_data)

    def process_all(self) -> None:
        """
        Execute complete processing pipeline.

        Steps:
            1. Filter adults
            2. Normalize names and emails
            3. Calculate scores
        """
        self.filter_adults()
        self._processed_data = process_user_data(self._raw_data)

    def get_results(self) -> List[Dict[str, Any]]:
        """
        Get the final processed user data.

        Returns:
            List[Dict]: Processed user records.
        """
        return self._processed_data.copy()

    def get_raw_data(self) -> List[Dict[str, Any]]:
        """
        Get the raw input data.

        Returns:
            List[Dict]: Original user records.
        """
        return self._raw_data.copy()


def save_user_info(user_id: int, user_info: str, db_path: str = "data.db") -> None:
    """
    Safely save user information to database.

    Security improvements:
        - Parameterized queries (prevents SQL injection)
        - Input validation
        - Resource management (context manager)
        - Error handling

    Args:
        user_id: Unique user identifier.
        user_info: User information string.
        db_path: Path to SQLite database file.

    Raises:
        ValueError: If inputs are invalid.
        sqlite3.Error: If database operation fails.

    Example:
        >>> save_user_info(1, "user@example.com")  # Safe and secure
    """
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("user_id must be a positive integer")

    if not isinstance(user_info, str) or not user_info.strip():
        raise ValueError("user_info must be a non-empty string")

    # Use context manager for automatic resource cleanup
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()

            # Parameterized query prevents SQL injection
            query = "INSERT INTO users (id, info) VALUES (?, ?)"
            cursor.execute(query, (user_id, user_info))

            # Connection automatically commits and closes
    except sqlite3.DatabaseError as e:
        raise sqlite3.Error(f"Failed to save user info: {e}")
