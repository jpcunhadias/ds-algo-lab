#!/usr/bin/env python3
"""
Simple test validation script to verify all tests can be imported and basic functionality works.
This doesn't require pytest to be installed.
"""

import sys
import traceback


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from src.data_structures import Array, LinkedList, Stack, Queue
        from src.algorithms.sorting import BubbleSort, InsertionSort, SelectionSort
        from src.algorithms.searching import LinearSearch, BinarySearch
        from src.visualization import DataStructureVisualizer, AlgorithmVisualizer
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False


def test_data_structures():
    """Test basic data structure operations."""
    print("\nTesting data structures...")
    try:
        from src.data_structures import Array, LinkedList, Stack, Queue

        # Test Array
        arr = Array([1, 2, 3])
        assert len(arr) == 3
        assert arr[0] == 1
        arr.append(4)
        assert len(arr) == 4
        print("✓ Array operations work")

        # Test LinkedList
        ll = LinkedList([1, 2, 3])
        assert len(ll) == 3
        assert ll[0] == 1
        ll.append(4)
        assert len(ll) == 4
        print("✓ LinkedList operations work")

        # Test Stack
        stack = Stack()
        stack.push(1)
        stack.push(2)
        assert stack.pop() == 2
        assert stack.pop() == 1
        print("✓ Stack operations work")

        # Test Queue
        queue = Queue()
        queue.enqueue(1)
        queue.enqueue(2)
        assert queue.dequeue() == 1
        assert queue.dequeue() == 2
        print("✓ Queue operations work")

        return True
    except Exception as e:
        print(f"✗ Data structure test failed: {e}")
        traceback.print_exc()
        return False


def test_algorithms():
    """Test basic algorithm operations."""
    print("\nTesting algorithms...")
    try:
        from src.data_structures import Array
        from src.algorithms.sorting import BubbleSort, InsertionSort, SelectionSort
        from src.algorithms.searching import LinearSearch, BinarySearch

        # Test sorting
        test_data = [3, 1, 4, 1, 5, 9, 2, 6]
        expected = [1, 1, 2, 3, 4, 5, 6, 9]

        arr1 = Array(test_data.copy())
        BubbleSort().execute(arr1, visualize=False)
        assert arr1.to_list() == expected
        print("✓ Bubble Sort works")

        arr2 = Array(test_data.copy())
        InsertionSort().execute(arr2, visualize=False)
        assert arr2.to_list() == expected
        print("✓ Insertion Sort works")

        arr3 = Array(test_data.copy())
        SelectionSort().execute(arr3, visualize=False)
        assert arr3.to_list() == expected
        print("✓ Selection Sort works")

        # Test searching
        arr = Array([1, 2, 3, 4, 5])
        searcher = LinearSearch()
        steps = searcher.execute(arr, 3, visualize=False)
        assert len(steps) > 0
        print("✓ Linear Search works")

        searcher2 = BinarySearch()
        steps2 = searcher2.execute(arr, 3, visualize=False)
        assert len(steps2) > 0
        print("✓ Binary Search works")

        return True
    except Exception as e:
        print(f"✗ Algorithm test failed: {e}")
        traceback.print_exc()
        return False


def test_visualization():
    """Test visualization imports and basic setup."""
    print("\nTesting visualization...")
    try:
        from src.visualization import DataStructureVisualizer, AlgorithmVisualizer
        from src.data_structures import Array

        visualizer = DataStructureVisualizer()
        arr = Array([1, 2, 3])
        visualizer.visualize(arr)
        print("✓ DataStructureVisualizer works")

        algo_visualizer = AlgorithmVisualizer()
        print("✓ AlgorithmVisualizer can be instantiated")

        return True
    except Exception as e:
        print(f"✗ Visualization test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all validation tests."""
    print("=" * 60)
    print("DSA Learning Platform - Test Validation")
    print("=" * 60)

    results = []
    results.append(("Imports", test_imports()))
    results.append(("Data Structures", test_data_structures()))
    results.append(("Algorithms", test_algorithms()))
    results.append(("Visualization", test_visualization()))

    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:20} {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 All validations passed!")
        print("\nNext steps:")
        print("1. Install pytest: pip install pytest")
        print("2. Run full test suite: pytest tests/ -v")
        print("3. Run examples: python examples/demo_array.py")
        return 0
    else:
        print("\n⚠️  Some validations failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

