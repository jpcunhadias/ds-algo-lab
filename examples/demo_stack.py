"""
Example: Stack Data Structure
Demonstrates LIFO operations on Stack with visualization.
"""

from src.data_structures.stack import Stack
from src.visualization.ds_visualizer import DataStructureVisualizer


def main():
    """Demonstrate Stack operations."""
    print("=== Stack Data Structure Demo ===\n")

    # Create a stack
    stack = Stack()
    print("Initial stack: Empty")

    # Create visualizer
    visualizer = DataStructureVisualizer()
    stack.attach_visualizer(visualizer)

    # Push operations
    print("\nPushing elements: 10, 20, 30")
    stack.push(10)
    stack.push(20)
    stack.push(30)
    print(f"Stack after pushes: {stack.to_list()}")
    visualizer.visualize(stack)
    visualizer.show()

    # Peek operation
    print(f"\nPeeking at top: {stack.peek()}")

    # Pop operations
    print("\nPopping elements:")
    while not stack.is_empty():
        value = stack.pop()
        print(f"  Popped: {value}")
        print(f"  Stack: {stack.to_list()}")
        if not stack.is_empty():
            visualizer.visualize(stack)
            visualizer.show()

    print("\n=== Demo Complete ===")


if __name__ == '__main__':
    main()

