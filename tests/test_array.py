"""
Unit tests for Array data structure.
"""

import pytest
from src.data_structures.array import Array


class TestArray:
    """Test cases for Array."""

    def test_init_empty(self):
        """Test initialization of empty array."""
        arr = Array()
        assert len(arr) == 0
        assert arr.to_list() == []

    def test_init_with_data(self):
        """Test initialization with initial data."""
        arr = Array([1, 2, 3])
        assert len(arr) == 3
        assert arr.to_list() == [1, 2, 3]

    def test_append(self):
        """Test append operation."""
        arr = Array()
        arr.append(1)
        arr.append(2)
        assert len(arr) == 2
        assert arr[0] == 1
        assert arr[1] == 2

    def test_insert(self):
        """Test insert operation."""
        arr = Array([1, 3])
        arr.insert(1, 2)
        assert arr.to_list() == [1, 2, 3]
        arr.insert(0, 0)
        assert arr.to_list() == [0, 1, 2, 3]

    def test_insert_invalid_index(self):
        """Test insert with invalid index."""
        arr = Array([1, 2])
        with pytest.raises(IndexError):
            arr.insert(5, 3)
        with pytest.raises(IndexError):
            arr.insert(-1, 0)

    def test_delete(self):
        """Test delete operation."""
        arr = Array([1, 2, 3])
        value = arr.delete(1)
        assert value == 2
        assert arr.to_list() == [1, 3]
        assert len(arr) == 2

    def test_delete_invalid_index(self):
        """Test delete with invalid index."""
        arr = Array([1, 2])
        with pytest.raises(IndexError):
            arr.delete(5)
        with pytest.raises(IndexError):
            arr.delete(-1)

    def test_search_found(self):
        """Test search when value is found."""
        arr = Array([1, 2, 3, 4, 5])
        assert arr.search(3) == 2
        assert arr.search(1) == 0
        assert arr.search(5) == 4

    def test_search_not_found(self):
        """Test search when value is not found."""
        arr = Array([1, 2, 3])
        assert arr.search(5) == -1

    def test_get(self):
        """Test get operation."""
        arr = Array([10, 20, 30])
        assert arr.get(0) == 10
        assert arr.get(1) == 20
        assert arr.get(2) == 30

    def test_get_invalid_index(self):
        """Test get with invalid index."""
        arr = Array([1, 2])
        with pytest.raises(IndexError):
            arr.get(5)

    def test_set(self):
        """Test set operation."""
        arr = Array([1, 2, 3])
        arr.set(1, 20)
        assert arr[1] == 20
        assert arr.to_list() == [1, 20, 3]

    def test_set_invalid_index(self):
        """Test set with invalid index."""
        arr = Array([1, 2])
        with pytest.raises(IndexError):
            arr.set(5, 10)

    def test_indexing(self):
        """Test indexing with [] operator."""
        arr = Array([1, 2, 3])
        assert arr[0] == 1
        assert arr[1] == 2
        arr[1] = 20
        assert arr[1] == 20

    def test_iteration(self):
        """Test iteration support."""
        arr = Array([1, 2, 3])
        result = [x for x in arr]
        assert result == [1, 2, 3]

    def test_contains(self):
        """Test 'in' operator."""
        arr = Array([1, 2, 3])
        assert 2 in arr
        assert 5 not in arr

    def test_repr(self):
        """Test string representation."""
        arr = Array([1, 2, 3])
        repr_str = repr(arr)
        assert 'Array' in repr_str

