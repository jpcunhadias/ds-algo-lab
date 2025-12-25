"""
Unit tests for searching algorithms.
"""

from src.algorithms.searching.binary_search import BinarySearch
from src.algorithms.searching.linear_search import LinearSearch
from src.data_structures.array import Array


class TestLinearSearch:
    """Test cases for Linear Search."""

    def test_search_found(self):
        """Test search when value is found."""
        arr = Array([1, 2, 3, 4, 5])
        searcher = LinearSearch()
        steps = searcher.execute(arr, 3, visualize=False)
        assert len(steps) > 0
        # Check that we found the value
        assert arr.search(3) == 2

    def test_search_not_found(self):
        """Test search when value is not found."""
        arr = Array([1, 2, 3, 4, 5])
        searcher = LinearSearch()
        steps = searcher.execute(arr, 10, visualize=False)
        assert len(steps) > 0

    def test_search_first_element(self):
        """Test search for first element."""
        arr = Array([1, 2, 3, 4, 5])
        searcher = LinearSearch()
        steps = searcher.execute(arr, 1, visualize=False)
        assert len(steps) > 0

    def test_search_last_element(self):
        """Test search for last element."""
        arr = Array([1, 2, 3, 4, 5])
        searcher = LinearSearch()
        steps = searcher.execute(arr, 5, visualize=False)
        assert len(steps) > 0

    def test_search_empty_array(self):
        """Test search in empty array."""
        arr = Array()
        searcher = LinearSearch()
        steps = searcher.execute(arr, 5, visualize=False)
        assert len(steps) > 0
        # Should complete without error even if target not found


class TestBinarySearch:
    """Test cases for Binary Search."""

    def test_search_found(self):
        """Test search when value is found."""
        arr = Array([1, 2, 3, 4, 5])
        searcher = BinarySearch()
        steps = searcher.execute(arr, 3, visualize=False)
        assert len(steps) > 0

    def test_search_not_found(self):
        """Test search when value is not found."""
        arr = Array([1, 2, 3, 4, 5])
        searcher = BinarySearch()
        steps = searcher.execute(arr, 10, visualize=False)
        assert len(steps) > 0

    def test_search_first_element(self):
        """Test search for first element."""
        arr = Array([1, 2, 3, 4, 5])
        searcher = BinarySearch()
        steps = searcher.execute(arr, 1, visualize=False)
        assert len(steps) > 0

    def test_search_last_element(self):
        """Test search for last element."""
        arr = Array([1, 2, 3, 4, 5])
        searcher = BinarySearch()
        steps = searcher.execute(arr, 5, visualize=False)
        assert len(steps) > 0

    def test_search_middle_element(self):
        """Test search for middle element."""
        arr = Array([1, 2, 3, 4, 5])
        searcher = BinarySearch()
        steps = searcher.execute(arr, 3, visualize=False)
        assert len(steps) > 0

    def test_search_sorted_array(self):
        """Test search in sorted array."""
        arr = Array([1, 3, 5, 7, 9, 11, 13])
        searcher = BinarySearch()
        steps = searcher.execute(arr, 7, visualize=False)
        assert len(steps) > 0
