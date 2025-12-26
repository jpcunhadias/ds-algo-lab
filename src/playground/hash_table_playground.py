"""
Hash Table playground for interactive exploration.
"""

from typing import List, Dict, Any, Optional
from .base import Playground


class HashTablePlayground(Playground):
    """
    Interactive playground for exploring hash table data structures.
    """

    def __init__(self, initial_capacity: int = 16, load_factor_threshold: float = 0.75):
        """
        Initialize hash table playground.

        Args:
            initial_capacity: Initial capacity
            load_factor_threshold: Load factor threshold for resizing
        """
        super().__init__("Hash Table Playground")
        from ..data_structures.hash_table import HashTable

        self.hash_table = HashTable(
            initial_capacity=initial_capacity, load_factor_threshold=load_factor_threshold
        )

    def set_input(self, data: List[Any], show_initialization: bool = True) -> None:
        """
        Set input data (bulk insert).

        Args:
            data: List of (key, value) tuples or just keys
            show_initialization: Whether to show initialization visualization (default: True)
        """
        self._initialization_steps = []
        step_counter = 0

        for item in data:
            if isinstance(item, tuple):
                key, value = item
            else:
                key, value = item, item  # Use same value as key

            # Get insertion steps
            steps = self.insert(key, value)
            # Renumber steps to be sequential across all insertions
            # Store a snapshot of hash table state for each step
            for step in steps:
                step_counter += 1
                step["step_number"] = step_counter
                step["initialization"] = True
                # Store snapshot of hash table state at this point
                if "data_structure" in step:
                    ht_state = step["data_structure"].get_state()
                    step["hash_table_state_snapshot"] = ht_state
                self._initialization_steps.append(step)

        # Add final state step
        if len(self._initialization_steps) > 0:
            step_counter += 1
            self._initialization_steps.append({
                "operation": "initialization_complete",
                "step_number": step_counter,
                "description": f"Hash table construction complete. Inserted {len(data)} items.",
                "data_structure": self.hash_table,
                "key": None,
                "value": None,
                "initialization": True,
            })

        if show_initialization and len(self._initialization_steps) > 0:
            self.visualize_initialization(interactive=True, auto_show=True)

    def insert(self, key: Any, value: Any) -> List[Dict[str, Any]]:
        """
        Insert a key-value pair.

        Args:
            key: Key to insert
            value: Value to insert

        Returns:
            List of operation steps
        """
        steps = []
        step_number = 0

        # Calculate hash
        hash_value = hash(key)
        bucket_index = hash_value % self.hash_table.get_capacity()

        step_number += 1
        steps.append(
            {
                "operation": "insert",
                "step_number": step_number,
                "description": f"Calculating hash for key {key}",
                "data_structure": self.hash_table,
                "key": key,
                "value": value,
                "bucket_index": bucket_index,
                "hash_value": hash_value,
            }
        )

        # Perform insertion
        self.hash_table.insert(key, value)

        step_number += 1
        steps.append(
            {
                "operation": "insert",
                "step_number": step_number,
                "description": f"Inserted {key}:{value} into bucket {bucket_index}",
                "data_structure": self.hash_table,
                "key": key,
                "value": value,
                "bucket_index": bucket_index,
                "hash_value": hash_value,
            }
        )

        # Check if resize occurred (compare with previous capacity)
        # Note: This is simplified - actual resize detection would need to track previous capacity
        # Resize visualization handled by hash table's internal notification

        return steps

    def get(self, key: Any) -> List[Dict[str, Any]]:
        """
        Get a value by key.

        Args:
            key: Key to search for

        Returns:
            List of operation steps
        """
        steps = []
        step_number = 0

        # Calculate hash
        hash_value = hash(key)
        bucket_index = hash_value % self.hash_table.get_capacity()

        step_number += 1
        steps.append(
            {
                "operation": "get",
                "step_number": step_number,
                "description": f"Searching for key {key}",
                "data_structure": self.hash_table,
                "key": key,
                "bucket_index": bucket_index,
                "hash_value": hash_value,
            }
        )

        # Perform get
        value = self.hash_table.get(key)
        found = value is not None

        step_number += 1
        steps.append(
            {
                "operation": "get",
                "step_number": step_number,
                "description": f"{'Found' if found else 'Not found'}: {key}",
                "data_structure": self.hash_table,
                "key": key,
                "value": value,
                "bucket_index": bucket_index,
                "hash_value": hash_value,
                "found": found,
            }
        )

        return steps

    def delete(self, key: Any) -> List[Dict[str, Any]]:
        """
        Delete a key-value pair.

        Args:
            key: Key to delete

        Returns:
            List of operation steps
        """
        steps = []
        step_number = 0

        # Calculate hash
        hash_value = hash(key)
        bucket_index = hash_value % self.hash_table.get_capacity()

        step_number += 1
        steps.append(
            {
                "operation": "delete",
                "step_number": step_number,
                "description": f"Deleting key {key}",
                "data_structure": self.hash_table,
                "key": key,
                "bucket_index": bucket_index,
                "hash_value": hash_value,
            }
        )

        # Perform deletion
        deleted = self.hash_table.delete(key)

        step_number += 1
        steps.append(
            {
                "operation": "delete",
                "step_number": step_number,
                "description": f"{'Deleted' if deleted else 'Not found'}: {key}",
                "data_structure": self.hash_table,
                "key": key,
                "bucket_index": bucket_index,
                "hash_value": hash_value,
            }
        )

        return steps

    def visualize_initialization(self, interactive: bool = True, auto_show: bool = True) -> None:
        """
        Visualize how input data was transformed into the hash table structure.

        Shows step-by-step hash calculation and bucket placement.

        Args:
            interactive: Whether to use interactive controls (True) or animated playback (False)
            auto_show: Whether to automatically show the visualization (for CLI integration)
        """
        if self._initialization_steps is None or len(self._initialization_steps) == 0:
            print("No initialization steps available. Hash table may not have been initialized with input data.")
            return

        print(f"\nBuilding hash table from input...")
        print(f"Capacity: {self.hash_table.get_capacity()}, Load Factor Threshold: {self.hash_table._load_factor_threshold}")
        print(f"Showing {len(self._initialization_steps)} initialization steps\n")

        self.visualize(self._initialization_steps, interactive=interactive)

    def visualize(self, steps: List[Dict[str, Any]], interactive: bool = True) -> None:
        """
        Visualize hash table operations.

        Args:
            steps: List of operation steps
            interactive: Whether to use interactive controls
        """
        if not steps:
            print("No steps to visualize")
            return

        from ..visualization.hash_table_visualizer import HashTableVisualizer

        visualizer = HashTableVisualizer()

        if interactive:
            from ..visualization.interactive_controls import InteractiveControls

            controls = InteractiveControls(steps, visualizer)
            controls.show()
        else:
            visualizer.animate(steps)

    def run_algorithm(self, algorithm_name: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Run a hash table operation.

        Args:
            algorithm_name: Operation name ('insert', 'get', 'delete')
            **kwargs: Operation-specific parameters

        Returns:
            List of operation steps
        """
        if algorithm_name == "insert":
            key = kwargs.get("key")
            value = kwargs.get("value")
            if key is None:
                raise ValueError("Insert operation requires 'key' parameter")
            if value is None:
                value = key  # Default value same as key
            return self.insert(key, value)
        elif algorithm_name == "get":
            key = kwargs.get("key")
            if key is None:
                raise ValueError("Get operation requires 'key' parameter")
            return self.get(key)
        elif algorithm_name == "delete":
            key = kwargs.get("key")
            if key is None:
                raise ValueError("Delete operation requires 'key' parameter")
            return self.delete(key)
        else:
            raise ValueError(f"Unknown operation: {algorithm_name}")

    def get_available_algorithms(self) -> List[str]:
        """
        Get list of available operations.

        Returns:
            List of operation names
        """
        return ["insert", "get", "delete"]

    def demo(self, operation: str = "insert", keys: Optional[List[Any]] = None) -> None:
        """
        Run a quick demonstration.

        Args:
            operation: Operation to demonstrate
            keys: Keys to use (random if None)
        """
        if keys is None:
            import random

            keys = [f"key{i}" for i in range(1, 11)]

        print(f"Hash Table Capacity: {self.hash_table.get_capacity()}")
        print(f"Load Factor Threshold: {self.hash_table._load_factor_threshold}")
        print(f"\nDemonstrating {operation} operations:")

        if operation == "insert":
            for key in keys:
                steps = self.insert(key, f"value_{key}")
                print(f"  Inserted {key}")

        print(f"\nHash Table Stats:")
        print(f"  Size: {len(self.hash_table)}")
        print(f"  Capacity: {self.hash_table.get_capacity()}")
        print(f"  Load Factor: {self.hash_table.get_load_factor():.2f}")

        # Visualize final state
        final_step = {
            "operation": "normal",
            "step_number": 1,
            "description": "Final hash table state",
            "data_structure": self.hash_table,
        }
        self.visualize([final_step], interactive=True)

