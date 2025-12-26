"""
Hash Table (Hash Map) data structure implementation.
A hash table with chaining collision resolution and visualization hooks.
"""

from typing import Any, Optional, List, Tuple, Dict
from ..visualization.base import BaseDataStructure


class HashTable(BaseDataStructure):
    """
    Hash Table implementation with visualization support.
    Uses chaining for collision resolution.
    """

    def __init__(self, initial_capacity: int = 16, load_factor_threshold: float = 0.75):
        """
        Initialize the hash table.

        Args:
            initial_capacity: Initial number of buckets
            load_factor_threshold: Load factor threshold for resizing
        """
        super().__init__()
        self._capacity = initial_capacity
        self._load_factor_threshold = load_factor_threshold
        self._buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(initial_capacity)]
        self._size = 0

        # Notify visualizer of initialization
        self._notify_visualizer('init', {
            'data_structure': self,
            'capacity': self._capacity,
            'load_factor_threshold': self._load_factor_threshold
        })

    def _hash(self, key: Any) -> int:
        """
        Hash function to compute bucket index.

        Args:
            key: The key to hash

        Returns:
            Bucket index
        """
        # Use Python's built-in hash function
        return hash(key) % self._capacity

    def _get_load_factor(self) -> float:
        """
        Calculate current load factor.

        Returns:
            Load factor (size / capacity)
        """
        return self._size / self._capacity if self._capacity > 0 else 0.0

    def _resize(self) -> None:
        """Resize the hash table when load factor exceeds threshold."""
        old_buckets = self._buckets
        old_capacity = self._capacity

        # Double the capacity
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

        # Rehash all existing key-value pairs
        for bucket in old_buckets:
            for key, value in bucket:
                self._set_internal(key, value, notify=False)

        self._notify_visualizer('resize', {
            'data_structure': self,
            'old_capacity': old_capacity,
            'new_capacity': self._capacity
        })

    def _set_internal(self, key: Any, value: Any, notify: bool = True) -> None:
        """
        Internal method to set a key-value pair without triggering resize check.

        Args:
            key: The key
            value: The value
            notify: Whether to notify visualizer
        """
        bucket_index = self._hash(key)
        bucket = self._buckets[bucket_index]

        # Check if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                if notify:
                    self._notify_visualizer('update', {
                        'data_structure': self,
                        'key': key,
                        'old_value': v,
                        'new_value': value,
                        'bucket_index': bucket_index
                    })
                return

        # Key doesn't exist, add new entry
        bucket.append((key, value))
        self._size += 1

        if notify:
            self._notify_visualizer('insert', {
                'data_structure': self,
                'key': key,
                'value': value,
                'bucket_index': bucket_index,
                'collision': len(bucket) > 1
            })

    def insert(self, key: Any, value: Any) -> None:
        """
        Insert or update a key-value pair.

        Args:
            key: The key
            value: The value
        """
        self._set_internal(key, value)

        # Check if resize is needed
        if self._get_load_factor() > self._load_factor_threshold:
            self._resize()

    def get(self, key: Any) -> Optional[Any]:
        """
        Get the value for a key.

        Args:
            key: The key

        Returns:
            The value if found, None otherwise
        """
        bucket_index = self._hash(key)
        bucket = self._buckets[bucket_index]

        for k, v in bucket:
            if k == key:
                self._notify_visualizer('get', {
                    'data_structure': self,
                    'key': key,
                    'value': v,
                    'bucket_index': bucket_index,
                    'found': True
                })
                return v

        self._notify_visualizer('get', {
            'data_structure': self,
            'key': key,
            'value': None,
            'bucket_index': bucket_index,
            'found': False
        })
        return None

    def delete(self, key: Any) -> bool:
        """
        Delete a key-value pair.

        Args:
            key: The key to delete

        Returns:
            True if key was deleted, False if not found
        """
        bucket_index = self._hash(key)
        bucket = self._buckets[bucket_index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                self._notify_visualizer('delete', {
                    'data_structure': self,
                    'key': key,
                    'value': v,
                    'bucket_index': bucket_index
                })
                return True

        self._notify_visualizer('delete', {
            'data_structure': self,
            'key': key,
            'found': False
        })
        return False

    def contains(self, key: Any) -> bool:
        """
        Check if a key exists in the hash table.

        Args:
            key: The key to check

        Returns:
            True if key exists, False otherwise
        """
        return self.get(key) is not None

    def get_load_factor(self) -> float:
        """
        Get the current load factor.

        Returns:
            Current load factor
        """
        return self._get_load_factor()

    def get_capacity(self) -> int:
        """
        Get the current capacity.

        Returns:
            Current capacity
        """
        return self._capacity

    def _get_internal_state(self) -> Dict[str, Any]:
        """
        Get the internal state representation.

        Returns:
            Dictionary representation of the hash table
        """
        buckets_data = []
        for i, bucket in enumerate(self._buckets):
            buckets_data.append({
                'index': i,
                'entries': [(str(k), v) for k, v in bucket],
                'size': len(bucket)
            })

        return {
            'capacity': self._capacity,
            'size': self._size,
            'load_factor': self._get_load_factor(),
            'buckets': buckets_data
        }

    def __len__(self) -> int:
        """Return the number of key-value pairs."""
        return self._size

    def __repr__(self) -> str:
        """String representation of the hash table."""
        return f"HashTable(size={self._size}, capacity={self._capacity}, load_factor={self._get_load_factor():.2f})"

