"""
Example: Using the Interactive Playground
Demonstrates the visual learning playground features.
"""

from src.playground.sorting_playground import SortingPlayground
from src.playground.searching_playground import SearchingPlayground
from src.playground.input_builder import InputBuilder
from src.visualization.comparison_viewer import ComparisonViewer
from src.data_structures.array import Array


def main():
    """Demonstrate playground features."""
    print("=== Interactive Playground Demo ===\n")

    # Sorting Playground
    print("--- Sorting Playground ---")
    pg = SortingPlayground()

    # Generate input
    input_data = [64, 34, 25, 12, 22, 11, 90]
    pg.set_input(input_data)
    print(f"Input: {input_data}")

    # Run algorithm
    steps = pg.run_algorithm('bubble_sort')
    print(f"Bubble Sort - Total steps: {len(steps)}")

    # Compare algorithms
    print("\nComparing algorithms...")
    pg.compare_algorithms(['bubble_sort', 'insertion_sort', 'selection_sort'])

    # Searching Playground
    print("\n--- Searching Playground ---")
    search_pg = SearchingPlayground()

    sorted_array = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    search_pg.set_input(sorted_array)
    search_pg.set_target(50)

    print(f"Array: {sorted_array}")
    print(f"Target: 50")

    steps = search_pg.run_algorithm('binary_search')
    print(f"Binary Search - Total steps: {len(steps)}")

    # Input Builder
    print("\n--- Input Builder ---")
    builder = InputBuilder()
    builder.from_string("5, 2, 8, 1, 9")
    print(f"Built array: {builder.get_data()}")

    arr = builder.to_array()
    print(f"Converted to Array: {arr.to_list()}")


if __name__ == '__main__':
    main()

