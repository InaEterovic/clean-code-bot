"""
Security module for input validation and sanitization.

Prevents prompt injection attacks and validates input safety.
"""

import re
from typing import Tuple, List
from pathlib import Path


class PromptInjectionDetector:
    """
    Detects potential prompt injection attempts in code input.
    
    Prevents attackers from injecting malicious instructions
    through code comments or strings.
    """

    # Patterns that might indicate prompt injection attempts
    SUSPICIOUS_PATTERNS = [
        r"(ignore|forget|override|bypass|disable|bypass|system.*prompt)",
        r"(instruction|command|directive).*:",
        r"('|\")\s*\+\s*[a-zA-Z_]",  # String concatenation with variables
        r"(\{|\[).*(\}|\])",  # Template/variable injection
        r"(eval|exec|__import__|compile|globals|locals)",  # Dynamic execution
    ]

    DANGEROUS_KEYWORDS = [
        "prompt_injection",
        "jailbreak",
        "bypass_filter",
        "ignore_system",
        "override_instruction",
    ]

    @staticmethod
    def detect_injection_patterns(code: str) -> Tuple[bool, List[str]]:
        """
        Detect potential prompt injection patterns in code.

        Args:
            code: The code to analyze.

        Returns:
            Tuple of (is_suspicious, list_of_detected_patterns).
        """
        detected_patterns = []
        code_lower = code.lower()

        # Check for dangerous keywords
        for keyword in PromptInjectionDetector.DANGEROUS_KEYWORDS:
            if keyword.lower() in code_lower:
                detected_patterns.append(f"Dangerous keyword: '{keyword}'")

        # Check for suspicious patterns
        for pattern in PromptInjectionDetector.SUSPICIOUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                detected_patterns.append(f"Suspicious pattern detected: {pattern}")

        return len(detected_patterns) > 0, detected_patterns

    @staticmethod
    def get_risk_level(code: str) -> str:
        """
        Assess the risk level of code input.

        Args:
            code: The code to assess.

        Returns:
            str: Risk level ("safe", "low", "medium", "high").
        """
        is_suspicious, patterns = PromptInjectionDetector.detect_injection_patterns(code)

        if not is_suspicious:
            return "safe"

        pattern_count = len(patterns)
        if pattern_count <= 1:
            return "low"
        elif pattern_count <= 3:
            return "medium"
        else:
            return "high"


class InputValidator:
    """
    Validates code input for safety and compliance.
    """

    # Maximum code size (10 MB)
    MAX_CODE_SIZE = 10 * 1024 * 1024

    # Maximum number of lines to process
    MAX_LINES = 10000

    @staticmethod
    def validate_code_input(code: str) -> Tuple[bool, str]:
        """
        Validate code input for safety and compliance.

        Args:
            code: The code to validate.

        Returns:
            Tuple of (is_valid, error_message).
        """
        # Check if code is empty
        if not code or not code.strip():
            return False, "Code input is empty"

        # Check code size
        if len(code.encode("utf-8")) > InputValidator.MAX_CODE_SIZE:
            return False, f"Code exceeds maximum size of {InputValidator.MAX_CODE_SIZE / 1024 / 1024:.1f} MB"

        # Check number of lines
        line_count = len(code.split("\n"))
        if line_count > InputValidator.MAX_LINES:
            return False, f"Code exceeds maximum of {InputValidator.MAX_LINES} lines"

        # Check for null bytes
        if "\x00" in code:
            return False, "Code contains null bytes"

        # Check for encoding issues
        try:
            code.encode("utf-8").decode("utf-8")
        except UnicodeEncodeError:
            return False, "Code contains invalid UTF-8 characters"

        return True, ""

    @staticmethod
    def validate_file_input(file_path: str) -> Tuple[bool, str]:
        """
        Validate file input for safety.

        Args:
            file_path: Path to the file to validate.

        Returns:
            Tuple of (is_valid, error_message).
        """
        path = Path(file_path)

        # Check if file exists
        if not path.exists():
            return False, f"File not found: {file_path}"

        # Check if it's a file (not directory)
        if not path.is_file():
            return False, f"Path is not a file: {file_path}"

        # Check file size
        file_size = path.stat().st_size
        if file_size > InputValidator.MAX_CODE_SIZE:
            return False, f"File exceeds maximum size of {InputValidator.MAX_CODE_SIZE / 1024 / 1024:.1f} MB"

        # Check file extension
        if path.suffix != ".py":
            return False, f"File must be a Python file (.py), got: {path.suffix}"

        return True, ""


class InputSanitizer:
    """
    Sanitizes and normalizes code input.
    """

    @staticmethod
    def sanitize_code(code: str) -> str:
        """
        Sanitize and normalize code.

        Args:
            code: The code to sanitize.

        Returns:
            str: Sanitized code.
        """
        # Remove null bytes
        code = code.replace("\x00", "")

        # Normalize line endings (convert to \n)
        code = code.replace("\r\n", "\n").replace("\r", "\n")

        # Remove leading/trailing whitespace
        code = code.strip()

        return code

    @staticmethod
    def remove_sensitive_patterns(code: str) -> str:
        """
        Remove or mask potentially sensitive patterns.

        Args:
            code: The code to process.

        Returns:
            str: Code with sensitive patterns removed/masked.
        """
        # Patterns for sensitive data (can be customized)
        sensitive_patterns = [
            (r"(api[_-]?key|apikey|password|secret|token|credential)\s*=\s*['\"]?[^'\"]*['\"]?",
             r"\1 = '***REDACTED***'"),
            (r"(https?://[^\s/'\"\\)]*:[^\s/'\"\\)]*@)",
             "***REDACTED***://***:***@"),
        ]

        sanitized = code
        for pattern, replacement in sensitive_patterns:
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)

        return sanitized

    @staticmethod
    def prepare_for_llm(code: str) -> str:
        """
        Prepare code for LLM processing.

        Performs comprehensive sanitization and validation.

        Args:
            code: The code to prepare.

        Returns:
            str: Prepared code, or empty string if invalid.
        """
        # Validate input
        is_valid, error_msg = InputValidator.validate_code_input(code)
        if not is_valid:
            raise ValueError(f"Invalid code input: {error_msg}")

        # Check for injection attempts
        is_suspicious, patterns = PromptInjectionDetector.detect_injection_patterns(code)
        if is_suspicious:
            risk_level = PromptInjectionDetector.get_risk_level(code)
            if risk_level == "high":
                raise ValueError(f"High-risk input detected. Refusing to process. Patterns: {patterns}")

        # Sanitize
        code = InputSanitizer.sanitize_code(code)

        # Remove/mask sensitive data
        code = InputSanitizer.remove_sensitive_patterns(code)

        return code
