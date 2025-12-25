"""
Example: Queue Data Structure
Demonstrates FIFO operations on Queue with visualization.
"""

from src.data_structures.queue import Queue
from src.visualization.ds_visualizer import DataStructureVisualizer


def main():
    """Demonstrate Queue operations."""
    print("=== Queue Data Structure Demo ===\n")

    # Create a queue
    queue = Queue()
    print("Initial queue: Empty")

    # Create visualizer
    visualizer = DataStructureVisualizer()
    queue.attach_visualizer(visualizer)

    # Enqueue operations
    print("\nEnqueuing elements: 10, 20, 30")
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    print(f"Queue after enqueues: {queue.to_list()}")
    visualizer.visualize(queue)
    visualizer.show()

    # Peek operation
    print(f"\nPeeking at front: {queue.peek()}")

    # Dequeue operations
    print("\nDequeuing elements:")
    while not queue.is_empty():
        value = queue.dequeue()
        print(f"  Dequeued: {value}")
        print(f"  Queue: {queue.to_list()}")
        if not queue.is_empty():
            visualizer.visualize(queue)
            visualizer.show()

    print("\n=== Demo Complete ===")


if __name__ == '__main__':
    main()

