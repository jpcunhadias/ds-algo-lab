"""
Ternary Search algorithm implementation with step tracking.
"""

from typing import List, Dict, Any
from ...visualization.base import BaseAlgorithm
from ...data_structures.array import Array


class TernarySearch(BaseAlgorithm):
    """
    Ternary Search algorithm with visualization support.
    Requires the array to be sorted.
    Divides the search space into three parts.
    """

    def __init__(self):
        """Initialize the ternary search algorithm."""
        super().__init__()
        self._name = "Ternary Search"

    def _run(self, data_structure):
        """
        Run the ternary search algorithm.

        Args:
            data_structure: Array to search in (must be sorted)

        Yields:
            Dictionary containing step information
        """
        # Get target from instance variable
        target = getattr(self, '_target', None)

        if target is None:
            return

        arr = data_structure
        step_number = 0

        left = 0
        right = len(arr) - 1

        step_number += 1

        # Yield step: initialization
        yield {
            'algorithm': self._name,
            'step_number': step_number,
            'description': f'Initializing ternary search for {target}',
            'data_structure': arr,
            'target': target,
            'current_index': -1,
            'found_index': -1,
            'left': left,
            'right': right,
            'mid1': -1,
            'mid2': -1
        }

        while left <= right:
            # Divide the search space into three parts
            mid1 = left + (right - left) // 3
            mid2 = right - (right - left) // 3

            step_number += 1

            # Yield step: checking mid1
            yield {
                'algorithm': self._name,
                'step_number': step_number,
                'description': f'Checking first third at index {mid1}: {arr[mid1]}',
                'data_structure': arr,
                'target': target,
                'current_index': mid1,
                'found_index': -1,
                'left': left,
                'right': right,
                'mid1': mid1,
                'mid2': mid2
            }

            if arr[mid1] == target:
                # Found at mid1!
                step_number += 1
                yield {
                    'algorithm': self._name,
                    'step_number': step_number,
                    'description': f'Found {target} at index {mid1}',
                    'data_structure': arr,
                    'target': target,
                    'current_index': mid1,
                    'found_index': mid1,
                    'left': left,
                    'right': right,
                    'mid1': mid1,
                    'mid2': mid2
                }
                return

            step_number += 1

            # Yield step: checking mid2
            yield {
                'algorithm': self._name,
                'step_number': step_number,
                'description': f'Checking second third at index {mid2}: {arr[mid2]}',
                'data_structure': arr,
                'target': target,
                'current_index': mid2,
                'found_index': -1,
                'left': left,
                'right': right,
                'mid1': mid1,
                'mid2': mid2
            }

            if arr[mid2] == target:
                # Found at mid2!
                step_number += 1
                yield {
                    'algorithm': self._name,
                    'step_number': step_number,
                    'description': f'Found {target} at index {mid2}',
                    'data_structure': arr,
                    'target': target,
                    'current_index': mid2,
                    'found_index': mid2,
                    'left': left,
                    'right': right,
                    'mid1': mid1,
                    'mid2': mid2
                }
                return

            # Determine which third to search
            if target < arr[mid1]:
                # Target is in first third
                step_number += 1
                yield {
                    'algorithm': self._name,
                    'step_number': step_number,
                    'description': f'{target} < {arr[mid1]}, searching first third',
                    'data_structure': arr,
                    'target': target,
                    'current_index': mid1,
                    'found_index': -1,
                    'left': left,
                    'right': mid1 - 1,
                    'mid1': mid1,
                    'mid2': mid2
                }
                right = mid1 - 1
            elif target > arr[mid2]:
                # Target is in third third
                step_number += 1
                yield {
                    'algorithm': self._name,
                    'step_number': step_number,
                    'description': f'{target} > {arr[mid2]}, searching third third',
                    'data_structure': arr,
                    'target': target,
                    'current_index': mid2,
                    'found_index': -1,
                    'left': mid2 + 1,
                    'right': right,
                    'mid1': mid1,
                    'mid2': mid2
                }
                left = mid2 + 1
            else:
                # Target is in middle third
                step_number += 1
                yield {
                    'algorithm': self._name,
                    'step_number': step_number,
                    'description': f'{arr[mid1]} < {target} < {arr[mid2]}, searching middle third',
                    'data_structure': arr,
                    'target': target,
                    'current_index': -1,
                    'found_index': -1,
                    'left': mid1 + 1,
                    'right': mid2 - 1,
                    'mid1': mid1,
                    'mid2': mid2
                }
                left = mid1 + 1
                right = mid2 - 1

        # Not found
        step_number += 1
        yield {
            'algorithm': self._name,
            'step_number': step_number,
            'description': f'{target} not found in array',
            'data_structure': arr,
            'target': target,
            'current_index': -1,
            'found_index': -1,
            'left': left,
            'right': right,
            'mid1': -1,
            'mid2': -1
        }

    def execute(self, data_structure, target: Any, visualize: bool = True) -> List[Dict[str, Any]]:
        """
        Execute ternary search for a target value.

        Args:
            data_structure: The array to search in (must be sorted)
            target: The value to search for
            visualize: Whether to visualize during execution

        Returns:
            List of execution steps
        """
        self._target = target
        return super().execute(data_structure, visualize)

