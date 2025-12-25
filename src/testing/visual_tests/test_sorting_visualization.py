"""
Visual test for sorting algorithm visualizations.
"""

from pathlib import Path

from src.algorithms.sorting.bubble_sort import BubbleSort
from src.algorithms.sorting.insertion_sort import InsertionSort
from src.algorithms.sorting.selection_sort import SelectionSort
from src.data_structures.array import Array
from src.visualization.algo_visualizer import AlgorithmVisualizer


def test_bubble_sort_visualization():
    """Test bubble sort visualization."""
    output_dir = Path(__file__).parent.parent.parent.parent / "test_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    arr = Array([64, 34, 25, 12, 22, 11, 90])
    visualizer = AlgorithmVisualizer()

    sorter = BubbleSort()
    sorter.attach_visualizer(visualizer)

    steps = sorter.execute(arr, visualize=False)

    # Visualize first few steps
    for i, step in enumerate(steps[:5]):
        visualizer.visualize(arr, step)
        output_file = output_dir / f"bubble_sort_step_{i + 1}.png"
        visualizer.save(str(output_file))
        print(f"Bubble sort step {i + 1} saved")


def test_insertion_sort_visualization():
    """Test insertion sort visualization."""
    output_dir = Path(__file__).parent.parent.parent.parent / "test_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    arr = Array([64, 34, 25, 12, 22, 11, 90])
    visualizer = AlgorithmVisualizer()

    sorter = InsertionSort()
    sorter.attach_visualizer(visualizer)

    steps = sorter.execute(arr, visualize=False)

    # Visualize first few steps
    for i, step in enumerate(steps[:5]):
        visualizer.visualize(arr, step)
        output_file = output_dir / f"insertion_sort_step_{i + 1}.png"
        visualizer.save(str(output_file))
        print(f"Insertion sort step {i + 1} saved")


def test_selection_sort_visualization():
    """Test selection sort visualization."""
    output_dir = Path(__file__).parent.parent.parent.parent / "test_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    arr = Array([64, 34, 25, 12, 22, 11, 90])
    visualizer = AlgorithmVisualizer()

    sorter = SelectionSort()
    sorter.attach_visualizer(visualizer)

    steps = sorter.execute(arr, visualize=False)

    # Visualize first few steps
    for i, step in enumerate(steps[:5]):
        visualizer.visualize(arr, step)
        output_file = output_dir / f"selection_sort_step_{i + 1}.png"
        visualizer.save(str(output_file))
        print(f"Selection sort step {i + 1} saved")


if __name__ == "__main__":
    test_bubble_sort_visualization()
    test_insertion_sort_visualization()
    test_selection_sort_visualization()
