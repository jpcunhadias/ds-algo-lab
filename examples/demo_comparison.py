"""
Example: Algorithm Comparison
Demonstrates side-by-side algorithm comparison.
"""

from src.data_structures.array import Array
from src.algorithms.sorting.bubble_sort import BubbleSort
from src.algorithms.sorting.insertion_sort import InsertionSort
from src.algorithms.sorting.selection_sort import SelectionSort
from src.visualization.comparison_viewer import ComparisonViewer


def main():
    """Demonstrate algorithm comparison."""
    print("=== Algorithm Comparison Demo ===\n")

    # Create test data
    input_data = [64, 34, 25, 12, 22, 11, 90]
    arr = Array(input_data.copy())

    print(f"Input: {input_data}\n")

    # Create comparison viewer
    viewer = ComparisonViewer()

    # Add algorithms
    viewer.add_algorithm(BubbleSort(), arr, "Bubble Sort")
    viewer.add_algorithm(InsertionSort(), arr, "Insertion Sort")
    viewer.add_algorithm(SelectionSort(), arr, "Selection Sort")

    # Show comparison
    print("Launching side-by-side comparison...")
    viewer.show()

    # Print performance metrics
    metrics = viewer.get_performance_metrics()
    print("\nPerformance Metrics:")
    print("=" * 50)
    for algo_name, metric in metrics.items():
        print(f"{algo_name}:")
        print(f"  Total Steps: {metric['total_steps']}")
        print(f"  Comparisons: {metric['comparisons']}")
        print(f"  Swaps: {metric['swaps']}")
        print()


if __name__ == '__main__':
    main()

