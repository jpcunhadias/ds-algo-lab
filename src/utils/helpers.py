"""
Helper utilities for the DSA Learning Platform.
"""

def validate_index(index, length, operation="access"):
    """
    Validate an index for array/list operations.

    Args:
        index: The index to validate
        length: The length of the data structure
        operation: The operation being performed (for error messages)

    Raises:
        IndexError: If index is out of bounds
    """
    if index < 0 or index >= length:
        raise IndexError(f"Index {index} out of bounds for {operation} (length: {length})")

