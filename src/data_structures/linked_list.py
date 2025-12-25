"""
Linked List data structure implementation.
A singly linked list with visualization hooks.
"""

from typing import Any, Optional, List
from ..visualization.base import BaseDataStructure


class ListNode:
    """
    Node class for linked list.
    """

    def __init__(self, value: Any):
        """
        Initialize a list node.

        Args:
            value: The value stored in the node
        """
        self.value = value
        self.next: Optional['ListNode'] = None

    def __repr__(self) -> str:
        """String representation of the node."""
        return f"ListNode({self.value})"


class LinkedList(BaseDataStructure):
    """
    Singly linked list implementation with visualization support.
    """

    def __init__(self, initial_data: Optional[List[Any]] = None):
        """
        Initialize the linked list.

        Args:
            initial_data: Optional initial data to populate the list
        """
        super().__init__()
        self._head: Optional[ListNode] = None
        self._size = 0

        # Build list from initial data
        if initial_data:
            for value in initial_data:
                self.append(value)

        # Notify visualizer of initialization
        self._notify_visualizer('init', {
            'data_structure': self,
            'initial_data': initial_data or []
        })

    def append(self, value: Any) -> None:
        """
        Append a value to the end of the linked list.

        Args:
            value: The value to append
        """
        new_node = ListNode(value)

        if self._head is None:
            self._head = new_node
        else:
            current = self._head
            while current.next is not None:
                current = current.next
            current.next = new_node

        self._size += 1
        self._notify_visualizer('append', {
            'data_structure': self,
            'value': value,
            'position': self._size - 1
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
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of bounds for insert (size: {self._size})")

        new_node = ListNode(value)

        if index == 0:
            new_node.next = self._head
            self._head = new_node
        else:
            current = self._head
            for _ in range(index - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node

        self._size += 1
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
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of bounds for delete (size: {self._size})")

        if index == 0:
            value = self._head.value
            self._head = self._head.next
        else:
            current = self._head
            for _ in range(index - 1):
                current = current.next
            value = current.next.value
            current.next = current.next.next

        self._size -= 1
        self._notify_visualizer('delete', {
            'data_structure': self,
            'index': index,
            'value': value
        })
        return value

    def search(self, value: Any) -> int:
        """
        Search for a value in the linked list.

        Args:
            value: The value to search for

        Returns:
            The index of the value, or -1 if not found
        """
        current = self._head
        index = 0

        while current is not None:
            if current.value == value:
                self._notify_visualizer('search', {
                    'data_structure': self,
                    'value': value,
                    'index': index,
                    'found': True
                })
                return index
            current = current.next
            index += 1

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
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of bounds for get (size: {self._size})")

        current = self._head
        for _ in range(index):
            current = current.next
        return current.value

    def traverse(self) -> List[Any]:
        """
        Traverse the linked list and return all values.

        Returns:
            List of all values in the linked list
        """
        values = []
        current = self._head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values

    def _get_internal_state(self) -> List[Any]:
        """
        Get the internal state representation.

        Returns:
            List of all values in the linked list
        """
        return self.traverse()

    def __len__(self) -> int:
        """Return the size of the linked list."""
        return self._size

    def __getitem__(self, index: int) -> Any:
        """Support indexing with []."""
        return self.get(index)

    def __iter__(self):
        """Support iteration."""
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def __contains__(self, value: Any) -> bool:
        """Support 'in' operator."""
        return self.search(value) != -1

    def to_list(self) -> List[Any]:
        """
        Convert the linked list to a Python list.

        Returns:
            List of all values
        """
        return self.traverse()

