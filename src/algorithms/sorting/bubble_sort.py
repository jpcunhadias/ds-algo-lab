"""
Bubble Sort algorithm implementation with step tracking.
"""

from ...data_structures.array import Array
from ...visualization.base import BaseAlgorithm


class BubbleSort(BaseAlgorithm):
    """
    Bubble Sort algorithm with visualization support.
    """

    def __init__(self):
        """Initialize the bubble sort algorithm."""
        super().__init__()
        self._name = "Bubble Sort"

    def _run(self, data_structure):
        """
        Run the bubble sort algorithm.

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

        for i in range(n):
            swapped = False

            for j in range(0, n - i - 1):
                step_number += 1

                # Yield step: comparing
                yield {
                    "algorithm": self._name,
                    "step_number": step_number,
                    "description": f"Comparing elements at indices {j} and {j + 1}",
                    "data_structure": Array(data.copy()),
                    "comparing": [j, j + 1],
                    "swapping": [],
                    "sorted": list(range(n - i, n)),
                    "current": [j],
                }

                if data[j] > data[j + 1]:
                    # Swap elements
                    data[j], data[j + 1] = data[j + 1], data[j]
                    swapped = True

                    step_number += 1

                    # Yield step: swapping
                    yield {
                        "algorithm": self._name,
                        "step_number": step_number,
                        "description": f"Swapping elements at indices {j} and {j + 1}",
                        "data_structure": Array(data.copy()),
                        "comparing": [j, j + 1],
                        "swapping": [j, j + 1],
                        "sorted": list(range(n - i, n)),
                        "current": [j],
                    }

            # Update the original data structure
            for k in range(n):
                arr.set(k, data[k])

            if not swapped:
                # Array is sorted, no more swaps needed
                break

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
