"""
Unit tests for Queue data structure.
"""

import pytest
from src.data_structures.queue import Queue


class TestQueue:
    """Test cases for Queue."""

    def test_init_empty(self):
        """Test initialization of empty queue."""
        queue = Queue()
        assert len(queue) == 0
        assert queue.is_empty()

    def test_init_with_data(self):
        """Test initialization with initial data."""
        queue = Queue([1, 2, 3])
        assert len(queue) == 3
        assert queue.to_list() == [1, 2, 3]

    def test_enqueue(self):
        """Test enqueue operation."""
        queue = Queue()
        queue.enqueue(1)
        queue.enqueue(2)
        assert len(queue) == 2
        assert queue.peek() == 1

    def test_dequeue(self):
        """Test dequeue operation."""
        queue = Queue([1, 2, 3])
        value = queue.dequeue()
        assert value == 1
        assert len(queue) == 2
        assert queue.peek() == 2

    def test_dequeue_empty(self):
        """Test dequeue from empty queue."""
        queue = Queue()
        with pytest.raises(IndexError):
            queue.dequeue()

    def test_peek(self):
        """Test peek operation."""
        queue = Queue([1, 2, 3])
        assert queue.peek() == 1
        assert len(queue) == 3  # Peek shouldn't remove

    def test_peek_empty(self):
        """Test peek on empty queue."""
        queue = Queue()
        with pytest.raises(IndexError):
            queue.peek()

    def test_is_empty(self):
        """Test is_empty operation."""
        queue = Queue()
        assert queue.is_empty()
        queue.enqueue(1)
        assert not queue.is_empty()
        queue.dequeue()
        assert queue.is_empty()

    def test_fifo_order(self):
        """Test FIFO (First In First Out) order."""
        queue = Queue()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        assert queue.dequeue() == 1
        assert queue.dequeue() == 2
        assert queue.dequeue() == 3

    def test_to_list(self):
        """Test to_list operation."""
        queue = Queue([1, 2, 3])
        assert queue.to_list() == [1, 2, 3]

