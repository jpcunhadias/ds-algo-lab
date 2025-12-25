"""
Example: Bubble Sort Algorithm
Demonstrates bubble sort with step-by-step visualization.
"""

from src.data_structures.array import Array
from src.algorithms.sorting.bubble_sort import BubbleSort
from src.visualization.algo_visualizer import AlgorithmVisualizer


def main():
    """Demonstrate Bubble Sort algorithm."""
    print("=== Bubble Sort Algorithm Demo ===\n")

    # Create an unsorted array
    arr = Array([64, 34, 25, 12, 22, 11, 90])
    print(f"Original array: {arr.to_list()}")

    # Create visualizer
    visualizer = AlgorithmVisualizer(animation_speed=0.5)

    # Create sorter
    sorter = BubbleSort()
    sorter.attach_visualizer(visualizer)

    # Execute sort with visualization
    print("\nSorting array...")
    steps = sorter.execute(arr, visualize=True)

    print(f"\nSorted array: {arr.to_list()}")
    print(f"Total steps: {len(steps)}")

    # Optionally, use step-by-step mode
    print("\n=== Step-by-Step Mode ===")
    print("Displaying steps one at a time...")
    visualizer.step_by_step(steps)

    print("\n=== Demo Complete ===")


if __name__ == '__main__':
    main()

