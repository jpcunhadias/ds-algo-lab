"""
Selection Sort algorithm implementation with step tracking.
"""

from ...data_structures.array import Array
from ...visualization.base import BaseAlgorithm


class SelectionSort(BaseAlgorithm):
    """
    Selection Sort algorithm with visualization support.
    """

    def __init__(self):
        """Initialize the selection sort algorithm."""
        super().__init__()
        self._name = "Selection Sort"

    def _run(self, data_structure):
        """
        Run the selection sort algorithm.

        Args:
            data_structure: Array to sort

        Yields:
            Dictionary containing step information
        """
        arr = data_structure
        n = len(arr)
        step_number = 0

        # Convert to list for easier manipulation
        data = arr.to_list()

        sorted_indices = []

        for i in range(n):
            # Find minimum element in remaining unsorted array
            min_idx = i

            step_number += 1

            # Yield step: starting new pass
            yield {
                "algorithm": self._name,
                "step_number": step_number,
                "description": f"Finding minimum element starting from index {i}",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [],
                "sorted": sorted_indices.copy(),
                "current": [i],
            }

            for j in range(i + 1, n):
                step_number += 1

                # Yield step: comparing
                yield {
                    "algorithm": self._name,
                    "step_number": step_number,
                    "description": f"Comparing {data[j]} with current minimum {data[min_idx]}",
                    "data_structure": Array(data.copy()),
                    "comparing": [j, min_idx],
                    "swapping": [],
                    "sorted": sorted_indices.copy(),
                    "current": [j, min_idx],
                }

                if data[j] < data[min_idx]:
                    min_idx = j

            # Swap the found minimum element with the first element
            if min_idx != i:
                step_number += 1

                # Yield step: swapping
                yield {
                    "algorithm": self._name,
                    "step_number": step_number,
                    "description": f"Swapping {data[i]} with minimum {data[min_idx]}",
                    "data_structure": Array(data.copy()),
                    "comparing": [],
                    "swapping": [i, min_idx],
                    "sorted": sorted_indices.copy(),
                    "current": [i, min_idx],
                }

                data[i], data[min_idx] = data[min_idx], data[i]

            sorted_indices.append(i)

            # Update the original data structure
            for k in range(n):
                arr.set(k, data[k])

            step_number += 1

            # Yield step: element in place
            yield {
                "algorithm": self._name,
                "step_number": step_number,
                "description": f"Element {data[i]} is now in its correct position",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [],
                "sorted": sorted_indices.copy(),
                "current": [i],
            }

        # Final step: sorted
        step_number += 1
        yield {
            "algorithm": self._name,
            "step_number": step_number,
            "description": "Array is now sorted",
            "data_structure": Array(data.copy()),
            "comparing": [],
            "swapping": [],
            "sorted": list(range(n)),
            "current": [],
        }
