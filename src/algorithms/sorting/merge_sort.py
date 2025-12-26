"""
Merge Sort algorithm implementation with step tracking.
"""

from ...data_structures.array import Array
from ...visualization.base import BaseAlgorithm


class MergeSort(BaseAlgorithm):
    """
    Merge Sort algorithm with visualization support.
    """

    def __init__(self):
        """Initialize the merge sort algorithm."""
        super().__init__()
        self._name = "Merge Sort"
        self._step_number = 0

    def _run(self, data_structure):
        """
        Run the merge sort algorithm.

        Args:
            data_structure: Array to sort

        Yields:
            Dictionary containing step information
        """
        arr = data_structure
        n = len(arr)
        self._step_number = 0

        # Convert to list for easier manipulation
        data = arr.to_list()

        # Track the current range being processed
        self._current_range = (0, n - 1)

        # Call recursive merge sort
        yield from self._merge_sort(data, 0, n - 1, arr)

        # Final step: sorted
        self._step_number += 1
        yield {
            "algorithm": self._name,
            "step_number": self._step_number,
            "description": "Array is now sorted",
            "data_structure": Array(data.copy()),
            "comparing": [],
            "swapping": [],
            "sorted": list(range(n)),
            "current": [],
            "merge": None,
            "left_range": None,
            "right_range": None,
        }

    def _merge_sort(self, data, left, right, arr):
        """
        Recursive merge sort function.

        Args:
            data: List to sort
            left: Left index
            right: Right index
            arr: Original Array object for updates

        Yields:
            Step dictionaries
        """
        if left < right:
            mid = (left + right) // 2

            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Dividing array from index {left} to {right} at {mid}",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [],
                "sorted": [],
                "current": list(range(left, right + 1)),
                "merge": None,
                "left_range": (left, mid),
                "right_range": (mid + 1, right),
            }

            # Sort left half
            yield from self._merge_sort(data, left, mid, arr)

            # Sort right half
            yield from self._merge_sort(data, mid + 1, right, arr)

            # Merge the sorted halves
            yield from self._merge(data, left, mid, right, arr)

    def _merge(self, data, left, mid, right, arr):
        """
        Merge two sorted subarrays.

        Args:
            data: List containing the subarrays
            left: Left index
            mid: Middle index
            right: Right index
            arr: Original Array object for updates

        Yields:
            Step dictionaries
        """
        # Create temporary arrays for left and right halves
        left_arr = data[left : mid + 1]
        right_arr = data[mid + 1 : right + 1]

        i = j = 0
        k = left

        comparing_indices = []

        self._step_number += 1
        yield {
            "algorithm": self._name,
            "step_number": self._step_number,
            "description": f"Merging sorted halves [{left}..{mid}] and [{mid+1}..{right}]",
            "data_structure": Array(data.copy()),
            "comparing": [],
            "swapping": [],
            "sorted": [],
            "current": list(range(left, right + 1)),
            "merge": {"left": left, "mid": mid, "right": right},
            "left_range": (left, mid),
            "right_range": (mid + 1, right),
        }

        # Merge the two arrays
        while i < len(left_arr) and j < len(right_arr):
            comparing_indices = [left + i, mid + 1 + j]

            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Comparing {left_arr[i]} and {right_arr[j]}",
                "data_structure": Array(data.copy()),
                "comparing": comparing_indices,
                "swapping": [],
                "sorted": [],
                "current": [k],
                "merge": {"left": left, "mid": mid, "right": right},
                "left_range": (left, mid),
                "right_range": (mid + 1, right),
            }

            if left_arr[i] <= right_arr[j]:
                data[k] = left_arr[i]
                i += 1
            else:
                data[k] = right_arr[j]
                j += 1

            # Update the original array
            arr.set(k, data[k])

            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Placed {data[k]} at position {k}",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [],
                "sorted": list(range(left, k + 1)),
                "current": [k],
                "merge": {"left": left, "mid": mid, "right": right},
                "left_range": (left, mid),
                "right_range": (mid + 1, right),
            }

            k += 1

        # Copy remaining elements from left_arr
        while i < len(left_arr):
            data[k] = left_arr[i]
            arr.set(k, data[k])

            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Copying remaining element {left_arr[i]} from left half",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [],
                "sorted": list(range(left, k + 1)),
                "current": [k],
                "merge": {"left": left, "mid": mid, "right": right},
                "left_range": (left, mid),
                "right_range": (mid + 1, right),
            }

            i += 1
            k += 1

        # Copy remaining elements from right_arr
        while j < len(right_arr):
            data[k] = right_arr[j]
            arr.set(k, data[k])

            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Copying remaining element {right_arr[j]} from right half",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [],
                "sorted": list(range(left, k + 1)),
                "current": [k],
                "merge": {"left": left, "mid": mid, "right": right},
                "left_range": (left, mid),
                "right_range": (mid + 1, right),
            }

            j += 1
            k += 1

        # Mark merged range as sorted
        self._step_number += 1
        yield {
            "algorithm": self._name,
            "step_number": self._step_number,
            "description": f"Completed merging range [{left}..{right}]",
            "data_structure": Array(data.copy()),
            "comparing": [],
            "swapping": [],
            "sorted": list(range(left, right + 1)),
            "current": [],
            "merge": None,
            "left_range": None,
            "right_range": None,
        }

