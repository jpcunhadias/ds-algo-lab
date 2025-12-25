"""
Example: Linked List Data Structure
Demonstrates basic operations on Linked List with visualization.
"""

from src.data_structures.linked_list import LinkedList
from src.visualization.ds_visualizer import DataStructureVisualizer


def main():
    """Demonstrate Linked List operations."""
    print("=== Linked List Data Structure Demo ===\n")

    # Create a linked list
    ll = LinkedList([1, 2, 3])
    print(f"Initial linked list: {ll.to_list()}")

    # Create visualizer
    visualizer = DataStructureVisualizer()
    ll.attach_visualizer(visualizer)

    # Visualize initial state
    print("\nVisualizing initial linked list...")
    visualizer.visualize(ll)
    visualizer.show()

    # Append operation
    print("\nAppending 4...")
    ll.append(4)
    print(f"Linked list after append: {ll.to_list()}")
    visualizer.visualize(ll)
    visualizer.show()

    # Insert operation
    print("\nInserting 10 at index 2...")
    ll.insert(2, 10)
    print(f"Linked list after insert: {ll.to_list()}")
    visualizer.visualize(ll)
    visualizer.show()

    # Search operation
    print("\nSearching for 10...")
    index = ll.search(10)
    print(f"Found at index: {index}")

    # Delete operation
    print("\nDeleting element at index 1...")
    value = ll.delete(1)
    print(f"Deleted value: {value}")
    print(f"Linked list after delete: {ll.to_list()}")
    visualizer.visualize(ll)
    visualizer.show()

    print("\n=== Demo Complete ===")


if __name__ == '__main__':
    main()

