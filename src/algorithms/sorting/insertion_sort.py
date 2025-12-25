"""
Insertion Sort algorithm implementation with step tracking.
"""

from ...data_structures.array import Array
from ...visualization.base import BaseAlgorithm


class InsertionSort(BaseAlgorithm):
    """
    Insertion Sort algorithm with visualization support.
    """

    def __init__(self):
        """Initialize the insertion sort algorithm."""
        super().__init__()
        self._name = "Insertion Sort"

    def _run(self, data_structure):
        """
        Run the insertion sort algorithm.

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

        # First element is considered sorted
        sorted_indices = [0]

        for i in range(1, n):
            key = data[i]
            j = i - 1

            step_number += 1

            # Yield step: selecting element to insert
            yield {
                "algorithm": self._name,
                "step_number": step_number,
                "description": f"Selecting element {key} at index {i} to insert",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [],
                "sorted": sorted_indices.copy(),
                "current": [i],
            }

            # Move elements greater than key one position ahead
            while j >= 0 and data[j] > key:
                step_number += 1

                # Yield step: comparing
                yield {
                    "algorithm": self._name,
                    "step_number": step_number,
                    "description": f"Comparing {data[j]} with {key}",
                    "data_structure": Array(data.copy()),
                    "comparing": [j, i],
                    "swapping": [],
                    "sorted": sorted_indices.copy(),
                    "current": [j, i],
                }

                data[j + 1] = data[j]
                j -= 1

            # Insert key at correct position
            data[j + 1] = key

            # Update sorted indices
            sorted_indices = list(range(i + 1))

            step_number += 1

            # Yield step: inserted
            yield {
                "algorithm": self._name,
                "step_number": step_number,
                "description": f"Inserted {key} at position {j + 1}",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [],
                "sorted": sorted_indices.copy(),
                "current": [j + 1],
            }

            # Update the original data structure
            for k in range(n):
                arr.set(k, data[k])

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
