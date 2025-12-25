"""
Code templates for implementing algorithms with visualization hooks.
"""

from typing import Dict, List


class AlgorithmTemplates:
    """
    Collection of algorithm templates for user implementation.
    """

    TEMPLATES = {
        'bubble_sort': """def bubble_sort(arr):
    \"\"\"
    Implement Bubble Sort algorithm.

    Args:
        arr: List to sort (will be modified in place)

    Returns:
        Sorted list
    \"\"\"
    n = len(arr)

    # Your implementation here
    # Hint: Compare adjacent elements and swap if needed
    # Repeat until no swaps occur

    return arr
""",

        'insertion_sort': """def insertion_sort(arr):
    \"\"\"
    Implement Insertion Sort algorithm.

    Args:
        arr: List to sort

    Returns:
        Sorted list
    \"\"\"
    # Your implementation here
    # Hint: Build sorted portion one element at a time
    # Insert each element into its correct position

    return arr
""",

        'selection_sort': """def selection_sort(arr):
    \"\"\"
    Implement Selection Sort algorithm.

    Args:
        arr: List to sort

    Returns:
        Sorted list
    \"\"\"
    # Your implementation here
    # Hint: Find minimum element and place at beginning
    # Repeat for remaining unsorted portion

    return arr
""",

        'linear_search': """def linear_search(arr, target):
    \"\"\"
    Implement Linear Search algorithm.

    Args:
        arr: List to search in
        target: Value to search for

    Returns:
        Index of target if found, -1 otherwise
    \"\"\"
    # Your implementation here
    # Hint: Check each element sequentially

    return -1
""",

        'binary_search': """def binary_search(arr, target):
    \"\"\"
    Implement Binary Search algorithm.
    Assumes arr is sorted.

    Args:
        arr: Sorted list to search in
        target: Value to search for

    Returns:
        Index of target if found, -1 otherwise
    \"\"\"
    # Your implementation here
    # Hint: Divide search space in half each iteration
    # Compare middle element with target

    return -1
""",
    }

    @classmethod
    def get_template(cls, algorithm_name: str) -> str:
        """
        Get template for an algorithm.

        Args:
            algorithm_name: Name of algorithm

        Returns:
            Template code string
        """
        return cls.TEMPLATES.get(algorithm_name, "# Template not available")

    @classmethod
    def list_templates(cls) -> List[str]:
        """
        List available templates.

        Returns:
            List of template names
        """
        return list(cls.TEMPLATES.keys())

    @classmethod
    def get_template_info(cls, algorithm_name: str) -> Dict[str, str]:
        """
        Get template information.

        Args:
            algorithm_name: Name of algorithm

        Returns:
            Dictionary with template info
        """
        template = cls.get_template(algorithm_name)
        return {
            'name': algorithm_name,
            'template': template,
            'description': template.split('"""')[1].strip() if '"""' in template else '',
        }

