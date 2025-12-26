"""
Binary Search algorithm implementation with step tracking.
"""

from typing import Any, Dict, List

from ...visualization.base import BaseAlgorithm


class BinarySearch(BaseAlgorithm):
    """
    Binary Search algorithm with visualization support.
    Requires the array to be sorted.
    """

    def __init__(self):
        """Initialize the binary search algorithm."""
        super().__init__()
        self._name = "Binary Search"

    def _run(self, data_structure):
        """
        Run the binary search algorithm.

        Args:
            data_structure: Array to search in (must be sorted)

        Yields:
            Dictionary containing step information
        """
        # Get target from instance variable
        target = getattr(self, "_target", None)

        if target is None:
            return

        arr = data_structure
        step_number = 0

        left = 0
        right = len(arr) - 1

        step_number += 1

        # Yield step: initialization
        yield {
            "algorithm": self._name,
            "step_number": step_number,
            "description": f"Initializing search for {target}",
            "data_structure": arr,
            "target": target,
            "current_index": -1,
            "found_index": -1,
            "left": left,
            "right": right,
            "mid": -1,
        }

        while left <= right:
            mid = (left + right) // 2

            step_number += 1

            # Yield step: checking middle element
            yield {
                "algorithm": self._name,
                "step_number": step_number,
                "description": f"Checking middle element at index {mid}: {arr[mid]}. "
                f"Search range: [{left}..{right}]. "
                f"Binary search divides the search space in half each iteration, giving O(log n) time complexity.",
                "data_structure": arr,
                "target": target,
                "current_index": mid,
                "found_index": -1,
                "left": left,
                "right": right,
                "mid": mid,
            }

            if arr[mid] == target:
                # Found!
                step_number += 1
                yield {
                    "algorithm": self._name,
                    "step_number": step_number,
                    "description": f"Found {target} at index {mid}! "
                    f"Binary search successfully located the target in {step_number} steps. "
                    f"This demonstrates the efficiency of divide-and-conquer approach.",
                    "data_structure": arr,
                    "target": target,
                    "current_index": mid,
                    "found_index": mid,
                    "left": left,
                    "right": right,
                    "mid": mid,
                }
                return
            elif arr[mid] < target:
                # Target is in right half
                step_number += 1
                yield {
                    "algorithm": self._name,
                    "step_number": step_number,
                    "description": f"{arr[mid]} < {target}, so target must be in the right half. "
                    f"Updating search range to [{mid + 1}..{right}]. "
                    f"We eliminate the left half since the array is sorted.",
                    "data_structure": arr,
                    "target": target,
                    "current_index": mid,
                    "found_index": -1,
                    "left": mid + 1,
                    "right": right,
                    "mid": mid,
                }
                left = mid + 1
            else:
                # Target is in left half
                step_number += 1
                yield {
                    "algorithm": self._name,
                    "step_number": step_number,
                    "description": f"{arr[mid]} > {target}, so target must be in the left half. "
                    f"Updating search range to [{left}..{mid - 1}]. "
                    f"We eliminate the right half since the array is sorted.",
                    "data_structure": arr,
                    "target": target,
                    "current_index": mid,
                    "found_index": -1,
                    "left": left,
                    "right": mid - 1,
                    "mid": mid,
                }
                right = mid - 1

        # Not found
        step_number += 1
        yield {
            "algorithm": self._name,
            "step_number": step_number,
            "description": f"{target} not found in array",
            "data_structure": arr,
            "target": target,
            "current_index": -1,
            "found_index": -1,
            "left": left,
            "right": right,
            "mid": -1,
        }

    def execute(
        self, data_structure, target: Any, visualize: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Execute binary search for a target value.

        Args:
            data_structure: The array to search in (must be sorted)
            target: The value to search for
            visualize: Whether to visualize during execution

        Returns:
            List of execution steps
        """
        self._target = target
        return super().execute(data_structure, visualize)
