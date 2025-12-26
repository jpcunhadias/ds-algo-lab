"""
Unit tests for sorting algorithms.
"""

import pytest
from src.data_structures.array import Array
from src.algorithms.sorting.bubble_sort import BubbleSort
from src.algorithms.sorting.insertion_sort import InsertionSort
from src.algorithms.sorting.selection_sort import SelectionSort
from src.algorithms.sorting.merge_sort import MergeSort
from src.algorithms.sorting.quick_sort import QuickSort
from src.algorithms.sorting.heap_sort import HeapSort


class TestBubbleSort:
    """Test cases for Bubble Sort."""

    def test_sort_sorted_array(self):
        """Test sorting an already sorted array."""
        arr = Array([1, 2, 3, 4, 5])
        sorter = BubbleSort()
        steps = sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 2, 3, 4, 5]
        assert len(steps) > 0

    def test_sort_reverse_array(self):
        """Test sorting a reverse sorted array."""
        arr = Array([5, 4, 3, 2, 1])
        sorter = BubbleSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 2, 3, 4, 5]

    def test_sort_unsorted_array(self):
        """Test sorting an unsorted array."""
        arr = Array([3, 1, 4, 1, 5, 9, 2, 6])
        sorter = BubbleSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 1, 2, 3, 4, 5, 6, 9]

    def test_sort_empty_array(self):
        """Test sorting an empty array."""
        arr = Array()
        sorter = BubbleSort()
        steps = sorter.execute(arr, visualize=False)
        assert arr.to_list() == []

    def test_sort_single_element(self):
        """Test sorting array with single element."""
        arr = Array([5])
        sorter = BubbleSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [5]


class TestInsertionSort:
    """Test cases for Insertion Sort."""

    def test_sort_sorted_array(self):
        """Test sorting an already sorted array."""
        arr = Array([1, 2, 3, 4, 5])
        sorter = InsertionSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 2, 3, 4, 5]

    def test_sort_reverse_array(self):
        """Test sorting a reverse sorted array."""
        arr = Array([5, 4, 3, 2, 1])
        sorter = InsertionSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 2, 3, 4, 5]

    def test_sort_unsorted_array(self):
        """Test sorting an unsorted array."""
        arr = Array([3, 1, 4, 1, 5, 9, 2, 6])
        sorter = InsertionSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 1, 2, 3, 4, 5, 6, 9]

    def test_sort_empty_array(self):
        """Test sorting an empty array."""
        arr = Array()
        sorter = InsertionSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == []

    def test_sort_single_element(self):
        """Test sorting array with single element."""
        arr = Array([5])
        sorter = InsertionSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [5]


class TestSelectionSort:
    """Test cases for Selection Sort."""

    def test_sort_sorted_array(self):
        """Test sorting an already sorted array."""
        arr = Array([1, 2, 3, 4, 5])
        sorter = SelectionSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 2, 3, 4, 5]

    def test_sort_reverse_array(self):
        """Test sorting a reverse sorted array."""
        arr = Array([5, 4, 3, 2, 1])
        sorter = SelectionSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 2, 3, 4, 5]

    def test_sort_unsorted_array(self):
        """Test sorting an unsorted array."""
        arr = Array([3, 1, 4, 1, 5, 9, 2, 6])
        sorter = SelectionSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 1, 2, 3, 4, 5, 6, 9]

    def test_sort_empty_array(self):
        """Test sorting an empty array."""
        arr = Array()
        sorter = SelectionSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == []

    def test_sort_single_element(self):
        """Test sorting array with single element."""
        arr = Array([5])
        sorter = SelectionSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [5]


class TestMergeSort:
    """Test cases for Merge Sort."""

    def test_sort_sorted_array(self):
        """Test sorting an already sorted array."""
        arr = Array([1, 2, 3, 4, 5])
        sorter = MergeSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 2, 3, 4, 5]

    def test_sort_reverse_array(self):
        """Test sorting a reverse sorted array."""
        arr = Array([5, 4, 3, 2, 1])
        sorter = MergeSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 2, 3, 4, 5]

    def test_sort_unsorted_array(self):
        """Test sorting an unsorted array."""
        arr = Array([3, 1, 4, 1, 5, 9, 2, 6])
        sorter = MergeSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 1, 2, 3, 4, 5, 6, 9]

    def test_sort_empty_array(self):
        """Test sorting an empty array."""
        arr = Array()
        sorter = MergeSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == []

    def test_sort_single_element(self):
        """Test sorting array with single element."""
        arr = Array([5])
        sorter = MergeSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [5]


class TestQuickSort:
    """Test cases for Quick Sort."""

    def test_sort_sorted_array(self):
        """Test sorting an already sorted array."""
        arr = Array([1, 2, 3, 4, 5])
        sorter = QuickSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 2, 3, 4, 5]

    def test_sort_reverse_array(self):
        """Test sorting a reverse sorted array."""
        arr = Array([5, 4, 3, 2, 1])
        sorter = QuickSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 2, 3, 4, 5]

    def test_sort_unsorted_array(self):
        """Test sorting an unsorted array."""
        arr = Array([3, 1, 4, 1, 5, 9, 2, 6])
        sorter = QuickSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 1, 2, 3, 4, 5, 6, 9]

    def test_sort_empty_array(self):
        """Test sorting an empty array."""
        arr = Array()
        sorter = QuickSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == []

    def test_sort_single_element(self):
        """Test sorting array with single element."""
        arr = Array([5])
        sorter = QuickSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [5]


class TestHeapSort:
    """Test cases for Heap Sort."""

    def test_sort_sorted_array(self):
        """Test sorting an already sorted array."""
        arr = Array([1, 2, 3, 4, 5])
        sorter = HeapSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 2, 3, 4, 5]

    def test_sort_reverse_array(self):
        """Test sorting a reverse sorted array."""
        arr = Array([5, 4, 3, 2, 1])
        sorter = HeapSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 2, 3, 4, 5]

    def test_sort_unsorted_array(self):
        """Test sorting an unsorted array."""
        arr = Array([3, 1, 4, 1, 5, 9, 2, 6])
        sorter = HeapSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [1, 1, 2, 3, 4, 5, 6, 9]

    def test_sort_empty_array(self):
        """Test sorting an empty array."""
        arr = Array()
        sorter = HeapSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == []

    def test_sort_single_element(self):
        """Test sorting array with single element."""
        arr = Array([5])
        sorter = HeapSort()
        sorter.execute(arr, visualize=False)
        assert arr.to_list() == [5]

