"""
Unit tests for Linked List data structure.
"""

import pytest
from src.data_structures.linked_list import LinkedList


class TestLinkedList:
    """Test cases for LinkedList."""

    def test_init_empty(self):
        """Test initialization of empty linked list."""
        ll = LinkedList()
        assert len(ll) == 0
        assert ll.to_list() == []

    def test_init_with_data(self):
        """Test initialization with initial data."""
        ll = LinkedList([1, 2, 3])
        assert len(ll) == 3
        assert ll.to_list() == [1, 2, 3]

    def test_append(self):
        """Test append operation."""
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        assert len(ll) == 2
        assert ll[0] == 1
        assert ll[1] == 2

    def test_insert(self):
        """Test insert operation."""
        ll = LinkedList([1, 3])
        ll.insert(1, 2)
        assert ll.to_list() == [1, 2, 3]
        ll.insert(0, 0)
        assert ll.to_list() == [0, 1, 2, 3]

    def test_insert_invalid_index(self):
        """Test insert with invalid index."""
        ll = LinkedList([1, 2])
        with pytest.raises(IndexError):
            ll.insert(5, 3)
        with pytest.raises(IndexError):
            ll.insert(-1, 0)

    def test_delete(self):
        """Test delete operation."""
        ll = LinkedList([1, 2, 3])
        value = ll.delete(1)
        assert value == 2
        assert ll.to_list() == [1, 3]
        assert len(ll) == 2

    def test_delete_invalid_index(self):
        """Test delete with invalid index."""
        ll = LinkedList([1, 2])
        with pytest.raises(IndexError):
            ll.delete(5)
        with pytest.raises(IndexError):
            ll.delete(-1)

    def test_search_found(self):
        """Test search when value is found."""
        ll = LinkedList([1, 2, 3, 4, 5])
        assert ll.search(3) == 2
        assert ll.search(1) == 0
        assert ll.search(5) == 4

    def test_search_not_found(self):
        """Test search when value is not found."""
        ll = LinkedList([1, 2, 3])
        assert ll.search(5) == -1

    def test_get(self):
        """Test get operation."""
        ll = LinkedList([10, 20, 30])
        assert ll.get(0) == 10
        assert ll.get(1) == 20
        assert ll.get(2) == 30

    def test_get_invalid_index(self):
        """Test get with invalid index."""
        ll = LinkedList([1, 2])
        with pytest.raises(IndexError):
            ll.get(5)

    def test_traverse(self):
        """Test traverse operation."""
        ll = LinkedList([1, 2, 3])
        assert ll.traverse() == [1, 2, 3]

    def test_indexing(self):
        """Test indexing with [] operator."""
        ll = LinkedList([1, 2, 3])
        assert ll[0] == 1
        assert ll[1] == 2

    def test_iteration(self):
        """Test iteration support."""
        ll = LinkedList([1, 2, 3])
        result = [x for x in ll]
        assert result == [1, 2, 3]

    def test_contains(self):
        """Test 'in' operator."""
        ll = LinkedList([1, 2, 3])
        assert 2 in ll
        assert 5 not in ll

