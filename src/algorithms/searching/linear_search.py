"""
Linear Search algorithm implementation with step tracking.
"""

from typing import List, Dict, Any
from ...visualization.base import BaseAlgorithm
from ...data_structures.array import Array


class LinearSearch(BaseAlgorithm):
    """
    Linear Search algorithm with visualization support.
    """

    def __init__(self):
        """Initialize the linear search algorithm."""
        super().__init__()
        self._name = "Linear Search"

    def _run(self, data_structure):
        """
        Run the linear search algorithm.

        Args:
            data_structure: Array to search in (must be sorted for binary search, but linear works on any)

        Yields:
            Dictionary containing step information
        """
        # Note: target should be passed via execute method
        # For now, we'll assume it's in the data_structure or passed separately
        # This is a simplified version - in practice, target would be a parameter

        # We need to get target from somewhere - let's assume it's stored
        # In a real implementation, we'd pass it as a parameter to execute()
        target = getattr(self, '_target', None)

        if target is None:
            # Default behavior: search for first element
            if len(data_structure) > 0:
                target = data_structure[0]
            else:
                return

        arr = data_structure
        step_number = 0

        for i in range(len(arr)):
            step_number += 1

            # Yield step: checking current element
            yield {
                'algorithm': self._name,
                'step_number': step_number,
                'description': f'Checking element at index {i}: {arr[i]}',
                'data_structure': arr,
                'target': target,
                'current_index': i,
                'found_index': -1
            }

            if arr[i] == target:
                # Found!
                step_number += 1
                yield {
                    'algorithm': self._name,
                    'step_number': step_number,
                    'description': f'Found {target} at index {i}',
                    'data_structure': arr,
                    'target': target,
                    'current_index': i,
                    'found_index': i
                }
                return

        # Not found
        step_number += 1
        yield {
            'algorithm': self._name,
            'step_number': step_number,
            'description': f'{target} not found in array',
            'data_structure': arr,
            'target': target,
            'current_index': -1,
            'found_index': -1
        }

    def execute(self, data_structure, target: Any, visualize: bool = True) -> List[Dict[str, Any]]:
        """
        Execute linear search for a target value.

        Args:
            data_structure: The array to search in
            target: The value to search for
            visualize: Whether to visualize during execution

        Returns:
            List of execution steps
        """
        self._target = target
        return super().execute(data_structure, visualize)

