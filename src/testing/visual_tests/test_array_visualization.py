"""
Visual test for Array data structure visualization.
"""

import os

from src.data_structures.array import Array
from src.visualization.ds_visualizer import DataStructureVisualizer


def test_array_visualization():
    """Test array visualization."""
    # Create output directory if it doesn't exist
    os.makedirs("test_outputs", exist_ok=True)

    # Create array
    arr = Array([1, 2, 3, 4, 5])

    # Create visualizer
    visualizer = DataStructureVisualizer()
    arr.attach_visualizer(visualizer)

    # Visualize initial state
    visualizer.visualize(arr)
    visualizer.save("test_outputs/array_initial.png")
    print("Array visualization saved to test_outputs/array_initial.png")

    # Perform operations
    arr.append(6)
    visualizer.visualize(arr)
    visualizer.save("test_outputs/array_after_append.png")
    print("Array after append saved to test_outputs/array_after_append.png")

    arr.insert(2, 10)
    visualizer.visualize(arr)
    visualizer.save("test_outputs/array_after_insert.png")
    print("Array after insert saved to test_outputs/array_after_insert.png")


if __name__ == "__main__":
    test_array_visualization()
