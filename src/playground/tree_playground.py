"""
Tree algorithm playground for interactive exploration.
Supports Binary Tree, BST, and AVL Tree.
"""

from typing import List, Dict, Any, Optional
from .base import Playground


class TreePlayground(Playground):
    """
    Interactive playground for exploring tree data structures.
    """

    def __init__(self, tree_type: str = "bst"):
        """
        Initialize tree playground.

        Args:
            tree_type: Type of tree ('binary_tree', 'bst', 'avl')
        """
        super().__init__(f"Tree Playground ({tree_type})")
        self.tree_type = tree_type
        self.tree = None
        self._initialize_tree()

    def _initialize_tree(self):
        """Initialize the tree based on type."""
        if self.tree_type == "binary_tree":
            from ..data_structures.binary_tree import BinaryTree

            self.tree = BinaryTree()
        elif self.tree_type == "bst":
            from ..data_structures.binary_search_tree import BinarySearchTree

            self.tree = BinarySearchTree()
        elif self.tree_type == "avl":
            from ..data_structures.avl_tree import AVLTree

            self.tree = AVLTree()
        else:
            raise ValueError(f"Unknown tree type: {self.tree_type}")

    def set_input(self, data: List[Any], show_initialization: bool = True) -> None:
        """
        Set input data (bulk insert).

        Args:
            data: List of values to insert
            show_initialization: Whether to show initialization visualization (default: True)
        """
        self._initialize_tree()
        self._initialization_steps = []
        step_counter = 0

        for value in data:
            # Get insertion steps
            steps = self.insert(value)
            # Renumber steps to be sequential across all insertions
            # Store a snapshot of tree state for each step
            for step in steps:
                step_counter += 1
                step["step_number"] = step_counter
                step["initialization"] = True
                # Store snapshot of tree state at this point
                if "data_structure" in step:
                    tree_state = step["data_structure"].get_state()
                    step["tree_state_snapshot"] = tree_state
                self._initialization_steps.append(step)

        # Add final state step
        step_counter += 1
        self._initialization_steps.append({
            "operation": "initialization_complete",
            "step_number": step_counter,
            "description": f"Tree construction complete. Inserted {len(data)} values.",
            "data_structure": self.tree,
            "current_node": None,
            "highlighted_nodes": [],
            "initialization": True,
        })

        if show_initialization and len(self._initialization_steps) > 0:
            self.visualize_initialization(interactive=True, auto_show=True)

    def insert(self, value: Any) -> List[Dict[str, Any]]:
        """
        Insert a value into the tree.

        Args:
            value: Value to insert

        Returns:
            List of operation steps
        """
        steps = []
        step_number = 0

        # Track insertion path (simplified - actual path depends on tree type)
        path = []
        if self.tree_type == "bst" or self.tree_type == "avl":
            # For BST/AVL, we can track the path
            path = self._get_insertion_path(value)

        step_number += 1
        steps.append(
            {
                "operation": "insert",
                "step_number": step_number,
                "description": f"Inserting {value}",
                "data_structure": self.tree,
                "current_node": value,
                "highlighted_nodes": path,
            }
        )

        # Perform insertion
        self.tree.insert(value)

        step_number += 1
        steps.append(
            {
                "operation": "insert",
                "step_number": step_number,
                "description": f"Inserted {value}",
                "data_structure": self.tree,
                "current_node": None,
                "highlighted_nodes": [],
            }
        )

        return steps

    def _get_insertion_path(self, value: Any) -> List[Any]:
        """
        Get the path that would be taken during insertion (for BST/AVL).

        Args:
            value: Value to insert

        Returns:
            List of node values in insertion path
        """
        path = []
        if self.tree_type == "bst":
            from ..data_structures.binary_search_tree import TreeNode

            def traverse(node, val):
                if node is None:
                    return
                path.append(node.value)
                if val < node.value:
                    traverse(node.left, val)
                elif val > node.value:
                    traverse(node.right, val)

            traverse(self.tree._root, value)
        elif self.tree_type == "avl":
            # Similar for AVL
            def traverse(node, val):
                if node is None:
                    return
                path.append(node.value)
                if val < node.value:
                    traverse(node.left, val)
                elif val > node.value:
                    traverse(node.right, val)

            traverse(self.tree._root, value)

        return path

    def delete(self, value: Any) -> List[Dict[str, Any]]:
        """
        Delete a value from the tree.

        Args:
            value: Value to delete

        Returns:
            List of operation steps
        """
        steps = []
        step_number = 0

        # Check if value exists
        if self.tree.search(value) is None:
            step_number += 1
            steps.append(
                {
                    "operation": "delete",
                    "step_number": step_number,
                    "description": f"Value {value} not found",
                    "data_structure": self.tree,
                    "current_node": None,
                    "highlighted_nodes": [],
                }
            )
            return steps

        # Get deletion path
        path = self._get_search_path(value)

        step_number += 1
        steps.append(
            {
                "operation": "delete",
                "step_number": step_number,
                "description": f"Deleting {value}",
                "data_structure": self.tree,
                "current_node": value,
                "highlighted_nodes": path,
            }
        )

        # Perform deletion
        self.tree.delete(value)

        step_number += 1
        steps.append(
            {
                "operation": "delete",
                "step_number": step_number,
                "description": f"Deleted {value}",
                "data_structure": self.tree,
                "current_node": None,
                "highlighted_nodes": [],
            }
        )

        return steps

    def _get_search_path(self, value: Any) -> List[Any]:
        """
        Get the path taken during search.

        Args:
            value: Value to search for

        Returns:
            List of node values in search path
        """
        path = []

        def traverse(node, val):
            if node is None:
                return False
            path.append(node.value)
            if node.value == val:
                return True
            if val < node.value:
                return traverse(node.left, val)
            else:
                return traverse(node.right, val)

        traverse(self.tree._root, value)
        return path

    def search(self, value: Any) -> List[Dict[str, Any]]:
        """
        Search for a value in the tree.

        Args:
            value: Value to search for

        Returns:
            List of operation steps
        """
        steps = []
        step_number = 0

        path = self._get_search_path(value)
        found = self.tree.search(value) is not None

        step_number += 1
        steps.append(
            {
                "operation": "search",
                "step_number": step_number,
                "description": f"Searching for {value}",
                "data_structure": self.tree,
                "current_node": value if found else None,
                "highlighted_nodes": path,
            }
        )

        return steps

    def traverse(self, traversal_type: str) -> List[Dict[str, Any]]:
        """
        Perform a tree traversal.

        Args:
            traversal_type: Type of traversal ('inorder', 'preorder', 'postorder', 'levelorder')

        Returns:
            List of operation steps
        """
        steps = []
        step_number = 0

        # Get traversal order
        if traversal_type == "inorder":
            traversal_order = self.tree.inorder_traversal()
        elif traversal_type == "preorder":
            traversal_order = self.tree.preorder_traversal()
        elif traversal_type == "postorder":
            traversal_order = self.tree.postorder_traversal()
        elif traversal_type == "levelorder":
            if hasattr(self.tree, "level_order_traversal"):
                traversal_order = self.tree.level_order_traversal()
            else:
                # Fallback for trees without level_order_traversal
                traversal_order = self.tree.inorder_traversal()
        else:
            raise ValueError(f"Unknown traversal type: {traversal_type}")

        # Create steps for each node in traversal
        for i, value in enumerate(traversal_order):
            step_number += 1
            steps.append(
                {
                    "operation": f"traversal_{traversal_type}",
                    "step_number": step_number,
                    "description": f"{traversal_type.title()} traversal: visiting {value}",
                    "data_structure": self.tree,
                    "current_node": value,
                    "traversal_path": traversal_order[: i + 1],
                    "highlighted_nodes": [value],
                }
            )

        return steps

    def visualize_initialization(self, interactive: bool = True, auto_show: bool = True) -> None:
        """
        Visualize how input data was transformed into the tree structure.

        Shows step-by-step tree construction with insertion paths.

        Args:
            interactive: Whether to use interactive controls (True) or animated playback (False)
            auto_show: Whether to automatically show the visualization (for CLI integration)
        """
        if self._initialization_steps is None or len(self._initialization_steps) == 0:
            print("No initialization steps available. Tree may not have been initialized with input data.")
            return

        print(f"\nBuilding {self.tree_type} tree from input...")
        print(f"Showing {len(self._initialization_steps)} initialization steps\n")

        self.visualize(self._initialization_steps, interactive=interactive)

    def visualize(self, steps: List[Dict[str, Any]], interactive: bool = True) -> None:
        """
        Visualize tree operations.

        Args:
            steps: List of operation steps
            interactive: Whether to use interactive controls
        """
        if not steps:
            print("No steps to visualize")
            return

        from ..visualization.tree_visualizer import TreeVisualizer

        visualizer = TreeVisualizer()

        if interactive:
            from ..visualization.interactive_controls import InteractiveControls

            controls = InteractiveControls(steps, visualizer)
            controls.show()
        else:
            visualizer.animate(steps)

    def run_algorithm(self, algorithm_name: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Run a tree operation.

        Args:
            algorithm_name: Operation name ('insert', 'delete', 'search', 'traverse')
            **kwargs: Operation-specific parameters

        Returns:
            List of operation steps
        """
        if algorithm_name == "insert":
            value = kwargs.get("value")
            if value is None:
                raise ValueError("Insert operation requires 'value' parameter")
            return self.insert(value)
        elif algorithm_name == "delete":
            value = kwargs.get("value")
            if value is None:
                raise ValueError("Delete operation requires 'value' parameter")
            return self.delete(value)
        elif algorithm_name == "search":
            value = kwargs.get("value")
            if value is None:
                raise ValueError("Search operation requires 'value' parameter")
            return self.search(value)
        elif algorithm_name == "traverse":
            traversal_type = kwargs.get("traversal_type", "inorder")
            return self.traverse(traversal_type)
        else:
            raise ValueError(f"Unknown operation: {algorithm_name}")

    def get_available_algorithms(self) -> List[str]:
        """
        Get list of available operations.

        Returns:
            List of operation names
        """
        return ["insert", "delete", "search", "traverse"]

    def demo(self, operation: str = "insert", values: Optional[List[Any]] = None) -> None:
        """
        Run a quick demonstration.

        Args:
            operation: Operation to demonstrate
            values: Values to use (random if None)
        """
        if values is None:
            import random

            values = random.sample(range(1, 20), 10)

        print(f"Tree Type: {self.tree_type}")
        print(f"Initial values: {values}")

        # Insert all values
        for value in values:
            steps = self.insert(value)
            if len(steps) > 0:
                print(f"Inserted {value}")

        # Show final tree
        print(f"\nTree size: {len(self.tree)}")
        print(f"In-order traversal: {self.tree.inorder_traversal()}")

        # Demonstrate traversal
        if operation == "traverse":
            print("\nDemonstrating traversals:")
            for trav_type in ["inorder", "preorder", "postorder", "levelorder"]:
                traversal = getattr(self.tree, f"{trav_type}_traversal")()
                print(f"  {trav_type}: {traversal}")

        # Visualize
        final_step = {
            "operation": "normal",
            "step_number": 1,
            "description": "Final tree state",
            "data_structure": self.tree,
            "current_node": None,
            "highlighted_nodes": [],
        }
        self.visualize([final_step], interactive=True)

