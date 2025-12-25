"""
Queue data structure implementation.
A FIFO (First In First Out) data structure with visualization hooks.
"""

from typing import Any, List, Optional

from ..visualization.base import BaseDataStructure


class Queue(BaseDataStructure):
    """
    Queue implementation using a list with visualization support.
    """

    def __init__(self, initial_data: Optional[List[Any]] = None):
        """
        Initialize the queue.

        Args:
            initial_data: Optional initial data to populate the queue
        """
        super().__init__()
        self._data = list(initial_data) if initial_data else []

        # Notify visualizer of initialization
        self._notify_visualizer(
            "init", {"data_structure": self, "initial_data": self._data.copy()}
        )

    def enqueue(self, value: Any) -> None:
        """
        Add a value to the rear of the queue.

        Args:
            value: The value to enqueue
        """
        self._data.append(value)
        self._notify_visualizer("enqueue", {"data_structure": self, "value": value})

    def dequeue(self) -> Any:
        """
        Remove and return the front value from the queue.

        Returns:
            The front value

        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from empty queue")

        value = self._data.pop(0)
        self._notify_visualizer("dequeue", {"data_structure": self, "value": value})
        return value

    def peek(self) -> Any:
        """
        Return the front value without removing it.

        Returns:
            The front value

        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Cannot peek at empty queue")

        return self._data[0]

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        Returns:
            True if empty, False otherwise
        """
        return len(self._data) == 0

    def _get_internal_state(self) -> List[Any]:
        """
        Get the internal state representation.

        Returns:
            Copy of the internal data list
        """
        return self._data.copy()

    def __len__(self) -> int:
        """Return the size of the queue."""
        return len(self._data)

    def __repr__(self) -> str:
        """String representation of the queue."""
        return f"Queue({self._data})"

    def to_list(self) -> List[Any]:
        """
        Convert the queue to a Python list (front to rear).

        Returns:
            A copy of the internal data as a list
        """
        return self._data.copy()
