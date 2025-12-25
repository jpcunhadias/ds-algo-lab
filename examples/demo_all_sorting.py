"""
Example: All Sorting Algorithms Comparison
Demonstrates all three sorting algorithms side by side.
"""

from src.data_structures.array import Array
from src.algorithms.sorting.bubble_sort import BubbleSort
from src.algorithms.sorting.insertion_sort import InsertionSort
from src.algorithms.sorting.selection_sort import SelectionSort


def main():
    """Compare all sorting algorithms."""
    print("=== Sorting Algorithms Comparison ===\n")

    # Test data
    test_data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array: {test_data}\n")

    # Bubble Sort
    print("--- Bubble Sort ---")
    arr1 = Array(test_data.copy())
    sorter1 = BubbleSort()
    steps1 = sorter1.execute(arr1, visualize=False)
    print(f"Sorted: {arr1.to_list()}")
    print(f"Steps: {len(steps1)}\n")

    # Insertion Sort
    print("--- Insertion Sort ---")
    arr2 = Array(test_data.copy())
    sorter2 = InsertionSort()
    steps2 = sorter2.execute(arr2, visualize=False)
    print(f"Sorted: {arr2.to_list()}")
    print(f"Steps: {len(steps2)}\n")

    # Selection Sort
    print("--- Selection Sort ---")
    arr3 = Array(test_data.copy())
    sorter3 = SelectionSort()
    steps3 = sorter3.execute(arr3, visualize=False)
    print(f"Sorted: {arr3.to_list()}")
    print(f"Steps: {len(steps3)}\n")

    # Verify all produce same result
    assert arr1.to_list() == arr2.to_list() == arr3.to_list()
    print("✓ All algorithms produce the same sorted result!")

    print("\n=== Demo Complete ===")


if __name__ == '__main__':
    main()

