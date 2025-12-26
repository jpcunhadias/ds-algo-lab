"""
Exponential Search algorithm implementation with step tracking.
"""

from typing import List, Dict, Any
from ...visualization.base import BaseAlgorithm
from ...data_structures.array import Array


class ExponentialSearch(BaseAlgorithm):
    """
    Exponential Search algorithm with visualization support.
    Requires the array to be sorted.
    First finds a range exponentially, then performs binary search.
    """

    def __init__(self):
        """Initialize the exponential search algorithm."""
        super().__init__()
        self._name = "Exponential Search"

    def _run(self, data_structure):
        """
        Run the exponential search algorithm.

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
        n = len(arr)

        step_number += 1

        # Yield step: initialization
        yield {
            'algorithm': self._name,
            'step_number': step_number,
            'description': f'Initializing exponential search for {target}',
            'data_structure': arr,
            'target': target,
            'current_index': -1,
            'found_index': -1,
            'left': 0,
            'right': n - 1,
            'range_start': 0,
            'range_end': -1,
            'phase': 'exponential_range_finding'
        }

        # If target is at first position
        if arr[0] == target:
            step_number += 1
            yield {
                'algorithm': self._name,
                'step_number': step_number,
                'description': f'Found {target} at index 0',
                'data_structure': arr,
                'target': target,
                'current_index': 0,
                'found_index': 0,
                'left': 0,
                'right': 0,
                'range_start': 0,
                'range_end': 0,
                'phase': 'found'
            }
            return

        # Find range by doubling index
        i = 1
        while i < n and arr[i] <= target:
            step_number += 1
            yield {
                'algorithm': self._name,
                'step_number': step_number,
                'description': f'Checking index {i}: {arr[i]}, expanding range exponentially',
                'data_structure': arr,
                'target': target,
                'current_index': i,
                'found_index': -1,
                'left': 0,
                'right': min(i * 2 - 1, n - 1),
                'range_start': i // 2,
                'range_end': min(i * 2 - 1, n - 1),
                'phase': 'exponential_range_finding'
            }

            if arr[i] == target:
                step_number += 1
                yield {
                    'algorithm': self._name,
                    'step_number': step_number,
                    'description': f'Found {target} at index {i} during range finding',
                    'data_structure': arr,
                    'target': target,
                    'current_index': i,
                    'found_index': i,
                    'left': i // 2,
                    'right': min(i * 2 - 1, n - 1),
                    'range_start': i // 2,
                    'range_end': min(i * 2 - 1, n - 1),
                    'phase': 'found'
                }
                return

            i *= 2

        # Determine the range for binary search
        range_start = i // 2
        range_end = min(i, n - 1)

        step_number += 1
        yield {
            'algorithm': self._name,
            'step_number': step_number,
            'description': f'Range found: [{range_start}..{range_end}], switching to binary search',
            'data_structure': arr,
            'target': target,
            'current_index': -1,
            'found_index': -1,
            'left': range_start,
            'right': range_end,
            'range_start': range_start,
            'range_end': range_end,
            'phase': 'binary_search'
        }

        # Perform binary search in the found range
        left = range_start
        right = range_end

        while left <= right:
            mid = (left + right) // 2

            step_number += 1
            yield {
                'algorithm': self._name,
                'step_number': step_number,
                'description': f'Binary search: checking middle element at index {mid}: {arr[mid]}',
                'data_structure': arr,
                'target': target,
                'current_index': mid,
                'found_index': -1,
                'left': left,
                'right': right,
                'range_start': range_start,
                'range_end': range_end,
                'phase': 'binary_search'
            }

            if arr[mid] == target:
                # Found!
                step_number += 1
                yield {
                    'algorithm': self._name,
                    'step_number': step_number,
                    'description': f'Found {target} at index {mid}',
                    'data_structure': arr,
                    'target': target,
                    'current_index': mid,
                    'found_index': mid,
                    'left': left,
                    'right': right,
                    'range_start': range_start,
                    'range_end': range_end,
                    'phase': 'found'
                }
                return
            elif arr[mid] < target:
                # Target is in right half
                step_number += 1
                yield {
                    'algorithm': self._name,
                    'step_number': step_number,
                    'description': f'{arr[mid]} < {target}, searching right half',
                    'data_structure': arr,
                    'target': target,
                    'current_index': mid,
                    'found_index': -1,
                    'left': mid + 1,
                    'right': right,
                    'range_start': range_start,
                    'range_end': range_end,
                    'phase': 'binary_search'
                }
                left = mid + 1
            else:
                # Target is in left half
                step_number += 1
                yield {
                    'algorithm': self._name,
                    'step_number': step_number,
                    'description': f'{arr[mid]} > {target}, searching left half',
                    'data_structure': arr,
                    'target': target,
                    'current_index': mid,
                    'found_index': -1,
                    'left': left,
                    'right': mid - 1,
                    'range_start': range_start,
                    'range_end': range_end,
                    'phase': 'binary_search'
                }
                right = mid - 1

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
            'range_start': range_start,
            'range_end': range_end,
            'phase': 'not_found'
        }

    def execute(self, data_structure, target: Any, visualize: bool = True) -> List[Dict[str, Any]]:
        """
        Execute exponential search for a target value.

        Args:
            data_structure: The array to search in (must be sorted)
            target: The value to search for
            visualize: Whether to visualize during execution

        Returns:
            List of execution steps
        """
        self._target = target
        return super().execute(data_structure, visualize)

