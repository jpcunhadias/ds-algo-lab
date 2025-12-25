"""
Example: Array Data Structure
Demonstrates basic operations on Array with visualization.
"""

from src.data_structures.array import Array
from src.visualization.ds_visualizer import DataStructureVisualizer


def main():
    """Demonstrate Array operations."""
    print("=== Array Data Structure Demo ===\n")

    # Create an array
    arr = Array([10, 20, 30])
    print(f"Initial array: {arr.to_list()}")

    # Create visualizer
    visualizer = DataStructureVisualizer()
    arr.attach_visualizer(visualizer)

    # Visualize initial state
    print("\nVisualizing initial array...")
    visualizer.visualize(arr)
    visualizer.show()

    # Append operation
    print("\nAppending 40...")
    arr.append(40)
    print(f"Array after append: {arr.to_list()}")
    visualizer.visualize(arr)
    visualizer.show()

    # Insert operation
    print("\nInserting 25 at index 2...")
    arr.insert(2, 25)
    print(f"Array after insert: {arr.to_list()}")
    visualizer.visualize(arr)
    visualizer.show()

    # Search operation
    print("\nSearching for 25...")
    index = arr.search(25)
    print(f"Found at index: {index}")

    # Delete operation
    print("\nDeleting element at index 1...")
    value = arr.delete(1)
    print(f"Deleted value: {value}")
    print(f"Array after delete: {arr.to_list()}")
    visualizer.visualize(arr)
    visualizer.show()

    print("\n=== Demo Complete ===")


if __name__ == '__main__':
    main()

