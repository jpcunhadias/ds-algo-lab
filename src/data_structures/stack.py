"""
Stack data structure implementation.
A LIFO (Last In First Out) data structure with visualization hooks.
"""

from typing import Any, List, Optional

from ..visualization.base import BaseDataStructure


class Stack(BaseDataStructure):
    """
    Stack implementation using a list with visualization support.
    """

    def __init__(self, initial_data: Optional[List[Any]] = None):
        """
        Initialize the stack.

        Args:
            initial_data: Optional initial data to populate the stack
        """
        super().__init__()
        self._data = list(initial_data) if initial_data else []

        # Notify visualizer of initialization
        self._notify_visualizer(
            "init", {"data_structure": self, "initial_data": self._data.copy()}
        )

    def push(self, value: Any) -> None:
        """
        Push a value onto the stack.

        Args:
            value: The value to push
        """
        self._data.append(value)
        self._notify_visualizer("push", {"data_structure": self, "value": value})

    def pop(self) -> Any:
        """
        Pop and return the top value from the stack.

        Returns:
            The top value

        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Cannot pop from empty stack")

        value = self._data.pop()
        self._notify_visualizer("pop", {"data_structure": self, "value": value})
        return value

    def peek(self) -> Any:
        """
        Return the top value without removing it.

        Returns:
            The top value

        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("Cannot peek at empty stack")

        return self._data[-1]

    def is_empty(self) -> bool:
        """
        Check if the stack is empty.

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
        """Return the size of the stack."""
        return len(self._data)

    def __repr__(self) -> str:
        """String representation of the stack."""
        return f"Stack({self._data})"

    def to_list(self) -> List[Any]:
        """
        Convert the stack to a Python list (top to bottom).

        Returns:
            A copy of the internal data as a list
        """
        return self._data.copy()
