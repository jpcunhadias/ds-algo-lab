"""
Example: Interactive Visualization Controls
Demonstrates play/pause/step controls for algorithm visualizations.
"""

from src.data_structures.array import Array
from src.algorithms.sorting.bubble_sort import BubbleSort
from src.visualization.interactive_controls import InteractiveControls
from src.visualization.algo_visualizer import AlgorithmVisualizer


def main():
    """Demonstrate interactive controls."""
    print("=== Interactive Controls Demo ===\n")

    # Create array and run algorithm
    arr = Array([64, 34, 25, 12, 22, 11, 90])
    print(f"Input: {arr.to_list()}")

    # Execute algorithm
    sorter = BubbleSort()
    steps = sorter.execute(arr, visualize=False)
    print(f"Total steps: {len(steps)}")

    # Create visualizer
    visualizer = AlgorithmVisualizer()

    # Show with interactive controls
    print("\nLaunching interactive visualization...")
    print("Use the controls to navigate through algorithm steps.")
    controls = InteractiveControls(steps, visualizer)
    controls.show()


if __name__ == '__main__':
    main()

