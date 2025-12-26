"""
Unified Data Structures Playground
Provides a common interface for all data structure playgrounds.
"""

from typing import List, Dict, Any, Optional
from .base import Playground
from .tree_playground import TreePlayground
from .graph_playground import GraphPlayground
from .hash_table_playground import HashTablePlayground


class UnifiedDSPlayground(Playground):
    """
    Unified interface for all data structure playgrounds.
    Provides operation history and common operations.
    """

    def __init__(self, ds_type: str, **kwargs):
        """
        Initialize unified data structure playground.

        Args:
            ds_type: Type of data structure ('tree', 'graph', 'hash_table')
            **kwargs: Type-specific parameters
        """
        super().__init__(f"Unified DS Playground ({ds_type})")
        self.ds_type = ds_type
        self.operation_history: List[Dict[str, Any]] = []

        # Initialize appropriate playground
        if ds_type == "tree":
            tree_type = kwargs.get("tree_type", "bst")
            self.playground = TreePlayground(tree_type=tree_type)
        elif ds_type == "graph":
            directed = kwargs.get("directed", False)
            self.playground = GraphPlayground(directed=directed)
        elif ds_type == "hash_table":
            capacity = kwargs.get("initial_capacity", 16)
            load_factor = kwargs.get("load_factor_threshold", 0.75)
            self.playground = HashTablePlayground(
                initial_capacity=capacity, load_factor_threshold=load_factor
            )
        else:
            raise ValueError(f"Unknown data structure type: {ds_type}")

    def set_input(self, data: List[Any]) -> None:
        """
        Set input data.

        Args:
            data: Input data list
        """
        self.playground.set_input(data)
        self.operation_history.append({"operation": "set_input", "data": data})

    def run_algorithm(self, algorithm_name: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Run an algorithm/operation.

        Args:
            algorithm_name: Name of algorithm/operation
            **kwargs: Algorithm-specific parameters

        Returns:
            List of operation steps
        """
        steps = self.playground.run_algorithm(algorithm_name, **kwargs)
        self.operation_history.append(
            {"operation": algorithm_name, "kwargs": kwargs, "steps": len(steps)}
        )
        return steps

    def visualize(self, steps: List[Dict[str, Any]], interactive: bool = True) -> None:
        """
        Visualize operations.

        Args:
            steps: List of operation steps
            interactive: Whether to use interactive controls
        """
        self.playground.visualize(steps, interactive=interactive)

    def get_available_algorithms(self) -> List[str]:
        """
        Get list of available algorithms/operations.

        Returns:
            List of algorithm names
        """
        return self.playground.get_available_algorithms()

    def get_operation_history(self) -> List[Dict[str, Any]]:
        """
        Get operation history.

        Returns:
            List of operations performed
        """
        return self.operation_history.copy()

    def undo(self) -> bool:
        """
        Undo last operation (simplified - would need state management).

        Returns:
            True if undo was successful
        """
        if self.operation_history:
            self.operation_history.pop()
            # In a full implementation, would restore previous state
            return True
        return False

