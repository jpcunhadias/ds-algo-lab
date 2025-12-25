"""
Visual input builder for creating test data.
"""

from typing import List, Any, Optional
from ..data_structures.array import Array


class InputBuilder:
    """
    Build input data visually or programmatically.
    """

    def __init__(self):
        """Initialize the input builder."""
        self.data: List[Any] = []

    def add_element(self, value: Any) -> None:
        """
        Add an element to the data.

        Args:
            value: Value to add
        """
        self.data.append(value)

    def insert_element(self, index: int, value: Any) -> None:
        """
        Insert element at index.

        Args:
            index: Index to insert at
            value: Value to insert
        """
        if 0 <= index <= len(self.data):
            self.data.insert(index, value)

    def remove_element(self, index: int) -> Any:
        """
        Remove element at index.

        Args:
            index: Index to remove

        Returns:
            Removed value
        """
        if 0 <= index < len(self.data):
            return self.data.pop(index)
        raise IndexError(f"Index {index} out of range")

    def update_element(self, index: int, value: Any) -> None:
        """
        Update element at index.

        Args:
            index: Index to update
            value: New value
        """
        if 0 <= index < len(self.data):
            self.data[index] = value
        else:
            raise IndexError(f"Index {index} out of range")

    def clear(self) -> None:
        """Clear all data."""
        self.data = []

    def set_data(self, data: List[Any]) -> None:
        """
        Set data directly.

        Args:
            data: Data to set
        """
        self.data = list(data)

    def get_data(self) -> List[Any]:
        """
        Get current data.

        Returns:
            Current data list
        """
        return self.data.copy()

    def to_array(self) -> Array:
        """
        Convert to Array data structure.

        Returns:
            Array instance
        """
        return Array(self.data.copy())

    def from_string(self, input_str: str, separator: str = ',') -> None:
        """
        Parse data from string.

        Args:
            input_str: String with comma-separated values
            separator: Separator character
        """
        try:
            self.data = [int(x.strip()) for x in input_str.split(separator) if x.strip()]
        except ValueError:
            # Try as floats
            try:
                self.data = [float(x.strip()) for x in input_str.split(separator) if x.strip()]
            except ValueError:
                # Keep as strings
                self.data = [x.strip() for x in input_str.split(separator) if x.strip()]

    def from_list(self, data: List[Any]) -> None:
        """
        Set data from list.

        Args:
            data: List of values
        """
        self.data = list(data)

    def visualize(self) -> None:
        """Visualize current data."""
        from ..visualization.ds_visualizer import DataStructureVisualizer

        arr = self.to_array()
        visualizer = DataStructureVisualizer()
        arr.attach_visualizer(visualizer)
        visualizer.visualize(arr)
        visualizer.show()

    def __len__(self) -> int:
        """Return length of data."""
        return len(self.data)

    def __repr__(self) -> str:
        """String representation."""
        return f"InputBuilder({self.data})"

