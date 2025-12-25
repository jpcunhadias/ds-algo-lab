"""
Array data structure implementation.
A dynamic array with visualization hooks.
"""

from typing import Any, List, Optional
from ..visualization.base import BaseDataStructure
from ..utils.helpers import validate_index


class Array(BaseDataStructure):
    """
    Dynamic array implementation with visualization support.
    """

    def __init__(self, initial_data: Optional[List[Any]] = None):
        """
        Initialize the array.

        Args:
            initial_data: Optional initial data to populate the array
        """
        super().__init__()
        self._data = list(initial_data) if initial_data else []

        # Notify visualizer of initialization
        self._notify_visualizer('init', {
            'data_structure': self,
            'initial_data': self._data.copy()
        })

    def append(self, value: Any) -> None:
        """
        Append a value to the end of the array.

        Args:
            value: The value to append
        """
        self._data.append(value)
        self._notify_visualizer('append', {
            'data_structure': self,
            'value': value,
            'index': len(self._data) - 1
        })

    def insert(self, index: int, value: Any) -> None:
        """
        Insert a value at a specific index.

        Args:
            index: The index to insert at
            value: The value to insert

        Raises:
            IndexError: If index is out of bounds
        """
        validate_index(index, len(self._data) + 1, "insert")
        self._data.insert(index, value)
        self._notify_visualizer('insert', {
            'data_structure': self,
            'index': index,
            'value': value
        })

    def delete(self, index: int) -> Any:
        """
        Delete and return the value at a specific index.

        Args:
            index: The index to delete

        Returns:
            The deleted value

        Raises:
            IndexError: If index is out of bounds
        """
        validate_index(index, len(self._data), "delete")
        value = self._data.pop(index)
        self._notify_visualizer('delete', {
            'data_structure': self,
            'index': index,
            'value': value
        })
        return value

    def search(self, value: Any) -> int:
        """
        Search for a value in the array.

        Args:
            value: The value to search for

        Returns:
            The index of the value, or -1 if not found
        """
        try:
            index = self._data.index(value)
            self._notify_visualizer('search', {
                'data_structure': self,
                'value': value,
                'index': index,
                'found': True
            })
            return index
        except ValueError:
            self._notify_visualizer('search', {
                'data_structure': self,
                'value': value,
                'index': -1,
                'found': False
            })
            return -1

    def get(self, index: int) -> Any:
        """
        Get the value at a specific index.

        Args:
            index: The index to access

        Returns:
            The value at the index

        Raises:
            IndexError: If index is out of bounds
        """
        validate_index(index, len(self._data), "get")
        return self._data[index]

    def set(self, index: int, value: Any) -> None:
        """
        Set the value at a specific index.

        Args:
            index: The index to set
            value: The new value

        Raises:
            IndexError: If index is out of bounds
        """
        validate_index(index, len(self._data), "set")
        old_value = self._data[index]
        self._data[index] = value
        self._notify_visualizer('update', {
            'data_structure': self,
            'index': index,
            'old_value': old_value,
            'new_value': value
        })

    def _get_internal_state(self) -> List[Any]:
        """
        Get the internal state representation.

        Returns:
            Copy of the internal data list
        """
        return self._data.copy()

    def __len__(self) -> int:
        """Return the length of the array."""
        return len(self._data)

    def __getitem__(self, index: int) -> Any:
        """Support indexing with []."""
        return self.get(index)

    def __setitem__(self, index: int, value: Any) -> None:
        """Support assignment with []."""
        self.set(index, value)

    def __iter__(self):
        """Support iteration."""
        return iter(self._data)

    def __contains__(self, value: Any) -> bool:
        """Support 'in' operator."""
        return value in self._data

    def to_list(self) -> List[Any]:
        """
        Convert the array to a Python list.

        Returns:
            A copy of the internal data as a list
        """
        return self._data.copy()

