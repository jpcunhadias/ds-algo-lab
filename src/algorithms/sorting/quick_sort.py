"""
Quick Sort algorithm implementation with step tracking.
"""

from ...data_structures.array import Array
from ...visualization.base import BaseAlgorithm


class QuickSort(BaseAlgorithm):
    """
    Quick Sort algorithm with visualization support.
    """

    def __init__(self):
        """Initialize the quick sort algorithm."""
        super().__init__()
        self._name = "Quick Sort"
        self._step_number = 0

    def _run(self, data_structure):
        """
        Run the quick sort algorithm.

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

        # Call recursive quick sort
        yield from self._quick_sort(data, 0, n - 1, arr)

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
            "pivot": None,
            "partition": None,
        }

    def _quick_sort(self, data, low, high, arr):
        """
        Recursive quick sort function.

        Args:
            data: List to sort
            low: Starting index
            high: Ending index
            arr: Original Array object for updates

        Yields:
            Step dictionaries
        """
        if low < high:
            # Partition the array and get pivot index
            pivot_idx = yield from self._partition(data, low, high, arr)

            # Sort elements before and after partition
            yield from self._quick_sort(data, low, pivot_idx - 1, arr)
            yield from self._quick_sort(data, pivot_idx + 1, high, arr)

    def _partition(self, data, low, high, arr):
        """
        Partition the array around a pivot element.

        Args:
            data: List to partition
            low: Starting index
            high: Ending index
            arr: Original Array object for updates

        Yields:
            Step dictionaries
        """
        # Choose rightmost element as pivot
        pivot = data[high]
        pivot_index = high

        self._step_number += 1
        yield {
            "algorithm": self._name,
            "step_number": self._step_number,
            "description": f"Selecting pivot: {pivot} at index {high}",
            "data_structure": Array(data.copy()),
            "comparing": [],
            "swapping": [],
            "sorted": [],
            "current": list(range(low, high + 1)),
            "pivot": pivot_index,
            "partition": {"low": low, "high": high},
        }

        # Index of smaller element (indicates right position of pivot)
        i = low - 1

        for j in range(low, high):
            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Comparing {data[j]} with pivot {pivot}",
                "data_structure": Array(data.copy()),
                "comparing": [j, pivot_index],
                "swapping": [],
                "sorted": [],
                "current": [j],
                "pivot": pivot_index,
                "partition": {"low": low, "high": high, "i": i},
            }

            # If current element is smaller than or equal to pivot
            if data[j] <= pivot:
                i += 1

                if i != j:
                    # Swap elements
                    data[i], data[j] = data[j], data[i]

                    # Update the original array
                    arr.set(i, data[i])
                    arr.set(j, data[j])

                    self._step_number += 1
                    yield {
                        "algorithm": self._name,
                        "step_number": self._step_number,
                        "description": f"Swapping {data[i]} and {data[j]}",
                        "data_structure": Array(data.copy()),
                        "comparing": [i, j],
                        "swapping": [i, j],
                        "sorted": [],
                        "current": [i, j],
                        "pivot": pivot_index,
                        "partition": {"low": low, "high": high, "i": i},
                    }
                else:
                    # Element is already in correct position relative to pivot
                    self._step_number += 1
                    yield {
                        "algorithm": self._name,
                        "step_number": self._step_number,
                        "description": f"{data[j]} is already in correct position",
                        "data_structure": Array(data.copy()),
                        "comparing": [],
                        "swapping": [],
                        "sorted": [],
                        "current": [j],
                        "pivot": pivot_index,
                        "partition": {"low": low, "high": high, "i": i},
                    }

        # Place pivot in correct position
        if i + 1 != high:
            data[i + 1], data[high] = data[high], data[i + 1]

            # Update the original array
            arr.set(i + 1, data[i + 1])
            arr.set(high, data[high])

            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Placing pivot {pivot} at final position {i + 1}",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [i + 1, high],
                "sorted": [i + 1],
                "current": [i + 1],
                "pivot": i + 1,
                "partition": {"low": low, "high": high},
            }
        else:
            # Pivot is already in correct position
            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Pivot {pivot} is already in correct position",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [],
                "sorted": [high],
                "current": [high],
                "pivot": high,
                "partition": {"low": low, "high": high},
            }

        # Return pivot index
        return i + 1

