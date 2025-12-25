"""
Visual test for search algorithm visualizations.
"""

import os
from src.data_structures.array import Array
from src.algorithms.searching.linear_search import LinearSearch
from src.algorithms.searching.binary_search import BinarySearch
from src.visualization.algo_visualizer import AlgorithmVisualizer


def test_linear_search_visualization():
    """Test linear search visualization."""
    os.makedirs('test_outputs', exist_ok=True)

    arr = Array([10, 20, 30, 40, 50, 60, 70])
    visualizer = AlgorithmVisualizer()

    searcher = LinearSearch()
    searcher.attach_visualizer(visualizer)

    steps = searcher.execute(arr, 40, visualize=False)

    # Visualize all steps
    for i, step in enumerate(steps):
        visualizer.visualize(arr, step)
        visualizer.save(f'test_outputs/linear_search_step_{i+1}.png')
        print(f"Linear search step {i+1} saved")


def test_binary_search_visualization():
    """Test binary search visualization."""
    os.makedirs('test_outputs', exist_ok=True)

    # Binary search requires sorted array
    arr = Array([10, 20, 30, 40, 50, 60, 70])
    visualizer = AlgorithmVisualizer()

    searcher = BinarySearch()
    searcher.attach_visualizer(visualizer)

    steps = searcher.execute(arr, 40, visualize=False)

    # Visualize all steps
    for i, step in enumerate(steps):
        visualizer.visualize(arr, step)
        visualizer.save(f'test_outputs/binary_search_step_{i+1}.png')
        print(f"Binary search step {i+1} saved")


if __name__ == '__main__':
    test_linear_search_visualization()
    test_binary_search_visualization()

