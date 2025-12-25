"""
Test data management for algorithms.
"""

from typing import List, Any, Dict
from ..playground.base import InputGenerator


class DataTestLibrary:
    """
    Library of interesting test cases for algorithms.
    """

    def __init__(self):
        """Initialize test data library."""
        self.test_cases = {
            'sorting': {
                'empty': [],
                'single': [1],
                'two_elements': [2, 1],
                'already_sorted': [1, 2, 3, 4, 5],
                'reverse_sorted': [5, 4, 3, 2, 1],
                'duplicates': [3, 1, 4, 1, 5, 9, 2, 6, 5],
                'negative': [-3, -1, -4, -2, -5],
                'mixed': [-2, 5, -1, 0, 3, -4],
                'large': list(range(1, 101)),
            },
            'searching': {
                'small': ([1, 3, 5, 7, 9], 5),
                'not_found': ([1, 3, 5, 7, 9], 4),
                'first': ([1, 3, 5, 7, 9], 1),
                'last': ([1, 3, 5, 7, 9], 9),
                'duplicates': ([1, 2, 2, 2, 3, 4], 2),
                'large': (list(range(1, 1001, 2)), 501),
            },
        }

    def get_sorting_test_case(self, name: str) -> List[Any]:
        """
        Get a sorting test case.

        Args:
            name: Name of test case

        Returns:
            Test data array
        """
        return self.test_cases['sorting'].get(name, [])

    def get_searching_test_case(self, name: str) -> tuple:
        """
        Get a searching test case.

        Args:
            name: Name of test case

        Returns:
            Tuple of (array, target)
        """
        return self.test_cases['searching'].get(name, ([], None))

    def list_sorting_cases(self) -> List[str]:
        """List available sorting test cases."""
        return list(self.test_cases['sorting'].keys())

    def list_searching_cases(self) -> List[str]:
        """List available searching test cases."""
        return list(self.test_cases['searching'].keys())

    def generate_edge_cases(self, algorithm_type: str, size: int = 10) -> Dict[str, List[Any]]:
        """
        Generate edge cases for testing.

        Args:
            algorithm_type: 'sorting' or 'searching'
            size: Size of test cases

        Returns:
            Dictionary of edge case names to test data
        """
        if algorithm_type == 'sorting':
            return {
                'empty': [],
                'single': [1],
                'all_same': [5] * size,
                'sorted': list(range(1, size + 1)),
                'reversed': list(range(size, 0, -1)),
                'nearly_sorted': InputGenerator.nearly_sorted(size),
                'many_duplicates': InputGenerator.duplicates(size, unique_values=3),
            }
        elif algorithm_type == 'searching':
            arr = list(range(1, size * 2 + 1, 2))  # Odd numbers
            return {
                'target_first': (arr, arr[0]),
                'target_last': (arr, arr[-1]),
                'target_middle': (arr, arr[len(arr)//2]),
                'target_not_found': (arr, arr[0] - 1),
                'target_too_large': (arr, arr[-1] + 1),
            }
        return {}

    def preview_test_case(self, algorithm_type: str, case_name: str) -> str:
        """
        Get a preview of a test case.

        Args:
            algorithm_type: 'sorting' or 'searching'
            case_name: Name of test case

        Returns:
            String preview
        """
        if algorithm_type == 'sorting':
            data = self.get_sorting_test_case(case_name)
            return f"Array: {data}\nLength: {len(data)}"
        elif algorithm_type == 'searching':
            arr, target = self.get_searching_test_case(case_name)
            return f"Array: {arr}\nTarget: {target}\nLength: {len(arr)}"
        return "Unknown test case"

