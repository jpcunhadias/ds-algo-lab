"""
Example: Binary Search Algorithm
Demonstrates binary search with step-by-step visualization.
"""

from src.data_structures.array import Array
from src.algorithms.searching.binary_search import BinarySearch
from src.visualization.algo_visualizer import AlgorithmVisualizer


def main():
    """Demonstrate Binary Search algorithm."""
    print("=== Binary Search Algorithm Demo ===\n")

    # Create a sorted array (binary search requires sorted array)
    arr = Array([10, 20, 30, 40, 50, 60, 70, 80, 90])
    print(f"Sorted array: {arr.to_list()}")

    # Create visualizer
    visualizer = AlgorithmVisualizer(animation_speed=0.5)

    # Create searcher
    searcher = BinarySearch()
    searcher.attach_visualizer(visualizer)

    # Search for a value
    target = 50
    print(f"\nSearching for: {target}")

    steps = searcher.execute(arr, target, visualize=True)

    # Check result
    found_index = arr.search(target)
    if found_index != -1:
        print(f"\nFound {target} at index: {found_index}")
    else:
        print(f"\n{target} not found in array")

    print(f"Total steps: {len(steps)}")

    # Try searching for a value not in array
    print("\n=== Searching for non-existent value ===")
    target2 = 45
    print(f"Searching for: {target2}")
    steps2 = searcher.execute(arr, target2, visualize=True)
    print(f"Total steps: {len(steps2)}")

    print("\n=== Demo Complete ===")


if __name__ == '__main__':
    main()

