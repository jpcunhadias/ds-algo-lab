"""
Heap Sort algorithm implementation with step tracking.
"""

from ...data_structures.array import Array
from ...visualization.base import BaseAlgorithm


class HeapSort(BaseAlgorithm):
    """
    Heap Sort algorithm with visualization support.
    """

    def __init__(self):
        """Initialize the heap sort algorithm."""
        super().__init__()
        self._name = "Heap Sort"
        self._step_number = 0

    def _run(self, data_structure):
        """
        Run the heap sort algorithm.

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

        # Build max heap
        yield from self._build_heap(data, n, arr)

        # Extract elements from heap one by one
        for i in range(n - 1, 0, -1):
            # Move root to end
            data[0], data[i] = data[i], data[0]

            # Update the original array
            arr.set(0, data[0])
            arr.set(i, data[i])

            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Moving root {data[i]} to sorted position {i}",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [0, i],
                "sorted": list(range(i, n)),
                "current": [0, i],
                "heap": {"size": i, "heap_indices": list(range(i))},
            }

            # Heapify root element
            yield from self._heapify(data, i, 0, arr)

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
            "heap": None,
        }

    def _build_heap(self, data, n, arr):
        """
        Build a max heap from the array.

        Args:
            data: List to heapify
            n: Size of the heap
            arr: Original Array object for updates

        Yields:
            Step dictionaries
        """
        self._step_number += 1
        yield {
            "algorithm": self._name,
            "step_number": self._step_number,
            "description": "Building max heap",
            "data_structure": Array(data.copy()),
            "comparing": [],
            "swapping": [],
            "sorted": [],
            "current": [],
            "heap": {"size": n, "heap_indices": list(range(n))},
        }

        # Start from the last non-leaf node and heapify each
        for i in range(n // 2 - 1, -1, -1):
            yield from self._heapify(data, n, i, arr)

        self._step_number += 1
        yield {
            "algorithm": self._name,
            "step_number": self._step_number,
            "description": "Max heap built successfully",
            "data_structure": Array(data.copy()),
            "comparing": [],
            "swapping": [],
            "sorted": [],
            "current": [],
            "heap": {"size": n, "heap_indices": list(range(n))},
        }

    def _heapify(self, data, heap_size, root_idx, arr):
        """
        Heapify a subtree rooted at root_idx.

        Args:
            data: List containing the heap
            heap_size: Size of the heap
            root_idx: Root index of the subtree
            arr: Original Array object for updates

        Yields:
            Step dictionaries
        """
        largest = root_idx
        left = 2 * root_idx + 1
        right = 2 * root_idx + 2

        comparing_indices = []

        # Check if left child exists and is greater than root
        if left < heap_size:
            comparing_indices = [root_idx, left]
            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Comparing root {data[root_idx]} with left child {data[left]}",
                "data_structure": Array(data.copy()),
                "comparing": comparing_indices,
                "swapping": [],
                "sorted": [],
                "current": [root_idx],
                "heap": {"size": heap_size, "heap_indices": list(range(heap_size)), "root": root_idx, "left": left, "right": right},
            }

            if data[left] > data[largest]:
                largest = left

        # Check if right child exists and is greater than largest so far
        if right < heap_size:
            comparing_indices = [largest, right]
            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Comparing {data[largest]} with right child {data[right]}",
                "data_structure": Array(data.copy()),
                "comparing": comparing_indices,
                "swapping": [],
                "sorted": [],
                "current": [largest],
                "heap": {"size": heap_size, "heap_indices": list(range(heap_size)), "root": root_idx, "left": left, "right": right},
            }

            if data[right] > data[largest]:
                largest = right

        # If largest is not root, swap and continue heapifying
        if largest != root_idx:
            data[root_idx], data[largest] = data[largest], data[root_idx]

            # Update the original array
            arr.set(root_idx, data[root_idx])
            arr.set(largest, data[largest])

            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Swapping {data[root_idx]} and {data[largest]} to maintain heap property",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [root_idx, largest],
                "sorted": [],
                "current": [root_idx, largest],
                "heap": {"size": heap_size, "heap_indices": list(range(heap_size)), "root": root_idx, "left": left, "right": right},
            }

            # Recursively heapify the affected subtree
            yield from self._heapify(data, heap_size, largest, arr)
        else:
            self._step_number += 1
            yield {
                "algorithm": self._name,
                "step_number": self._step_number,
                "description": f"Heap property satisfied at index {root_idx}",
                "data_structure": Array(data.copy()),
                "comparing": [],
                "swapping": [],
                "sorted": [],
                "current": [root_idx],
                "heap": {"size": heap_size, "heap_indices": list(range(heap_size)), "root": root_idx},
            }

