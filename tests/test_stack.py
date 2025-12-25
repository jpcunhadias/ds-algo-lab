"""
Unit tests for Stack data structure.
"""

import pytest
from src.data_structures.stack import Stack


class TestStack:
    """Test cases for Stack."""

    def test_init_empty(self):
        """Test initialization of empty stack."""
        stack = Stack()
        assert len(stack) == 0
        assert stack.is_empty()

    def test_init_with_data(self):
        """Test initialization with initial data."""
        stack = Stack([1, 2, 3])
        assert len(stack) == 3
        assert stack.to_list() == [1, 2, 3]

    def test_push(self):
        """Test push operation."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        assert len(stack) == 2
        assert stack.peek() == 2

    def test_pop(self):
        """Test pop operation."""
        stack = Stack([1, 2, 3])
        value = stack.pop()
        assert value == 3
        assert len(stack) == 2
        assert stack.peek() == 2

    def test_pop_empty(self):
        """Test pop from empty stack."""
        stack = Stack()
        with pytest.raises(IndexError):
            stack.pop()

    def test_peek(self):
        """Test peek operation."""
        stack = Stack([1, 2, 3])
        assert stack.peek() == 3
        assert len(stack) == 3  # Peek shouldn't remove

    def test_peek_empty(self):
        """Test peek on empty stack."""
        stack = Stack()
        with pytest.raises(IndexError):
            stack.peek()

    def test_is_empty(self):
        """Test is_empty operation."""
        stack = Stack()
        assert stack.is_empty()
        stack.push(1)
        assert not stack.is_empty()
        stack.pop()
        assert stack.is_empty()

    def test_lifo_order(self):
        """Test LIFO (Last In First Out) order."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        assert stack.pop() == 3
        assert stack.pop() == 2
        assert stack.pop() == 1

    def test_to_list(self):
        """Test to_list operation."""
        stack = Stack([1, 2, 3])
        assert stack.to_list() == [1, 2, 3]

