"""
AVL Tree (Self-Balancing Binary Search Tree) data structure implementation.
An AVL tree with rotation operations and visualization hooks.
"""

from typing import Any, Optional, List
from .binary_tree import TreeNode
from ..visualization.base import BaseDataStructure


class AVLTree(BaseDataStructure):
    """
    AVL Tree implementation with visualization support.
    Maintains BST property and AVL balance property.
    """

    def __init__(self, initial_data: Optional[List[Any]] = None):
        """
        Initialize the AVL tree.

        Args:
            initial_data: Optional initial data to populate the tree
        """
        super().__init__()
        self._root: Optional[TreeNode] = None
        self._size = 0

        # Build tree from initial data
        if initial_data:
            for value in initial_data:
                self.insert(value)

        # Notify visualizer of initialization
        self._notify_visualizer('init', {
            'data_structure': self,
            'initial_data': initial_data or []
        })

    def _height(self, node: Optional[TreeNode]) -> int:
        """
        Get the height of a node.

        Args:
            node: The node

        Returns:
            Height of the node (-1 for None)
        """
        if node is None:
            return -1
        return max(self._height(node.left), self._height(node.right)) + 1

    def _balance_factor(self, node: Optional[TreeNode]) -> int:
        """
        Calculate the balance factor of a node.

        Args:
            node: The node

        Returns:
            Balance factor (height of left subtree - height of right subtree)
        """
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, y: TreeNode) -> TreeNode:
        """
        Right rotation.

        Args:
            y: The node to rotate around

        Returns:
            New root of the subtree
        """
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        self._notify_visualizer('rotate', {
            'data_structure': self,
            'rotation_type': 'right',
            'pivot': y.value,
            'new_root': x.value
        })

        return x

    def _rotate_left(self, x: TreeNode) -> TreeNode:
        """
        Left rotation.

        Args:
            x: The node to rotate around

        Returns:
            New root of the subtree
        """
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        self._notify_visualizer('rotate', {
            'data_structure': self,
            'rotation_type': 'left',
            'pivot': x.value,
            'new_root': y.value
        })

        return y

    def _rotate_left_right(self, z: TreeNode) -> TreeNode:
        """
        Left-right rotation (double rotation).

        Args:
            z: The node to rotate around

        Returns:
            New root of the subtree
        """
        z.left = self._rotate_left(z.left)
        return self._rotate_right(z)

    def _rotate_right_left(self, z: TreeNode) -> TreeNode:
        """
        Right-left rotation (double rotation).

        Args:
            z: The node to rotate around

        Returns:
            New root of the subtree
        """
        z.right = self._rotate_right(z.right)
        return self._rotate_left(z)

    def insert(self, value: Any) -> None:
        """
        Insert a value into the AVL tree maintaining balance.

        Args:
            value: The value to insert
        """
        self._root = self._insert_recursive(self._root, value)
        self._size += 1
        self._notify_visualizer('insert', {
            'data_structure': self,
            'value': value
        })

    def _insert_recursive(self, node: Optional[TreeNode], value: Any) -> TreeNode:
        """
        Recursive helper for insert with balancing.

        Args:
            node: Current node
            value: Value to insert

        Returns:
            Updated node
        """
        # Standard BST insert
        if node is None:
            return TreeNode(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            # Duplicate values not allowed
            return node

        # Update balance factor
        balance = self._balance_factor(node)

        # Left Left Case
        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)

        # Right Right Case
        if balance < -1 and value > node.right.value:
            return self._rotate_left(node)

        # Left Right Case
        if balance > 1 and value > node.left.value:
            return self._rotate_left_right(node)

        # Right Left Case
        if balance < -1 and value < node.right.value:
            return self._rotate_right_left(node)

        return node

    def search(self, value: Any) -> Optional[TreeNode]:
        """
        Search for a value in the AVL tree.

        Args:
            value: The value to search for

        Returns:
            The node containing the value, or None if not found
        """
        return self._search_recursive(self._root, value)

    def _search_recursive(self, node: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
        """
        Recursive helper for search.

        Args:
            node: Current node
            value: Value to search for

        Returns:
            Node containing value or None
        """
        if node is None or node.value == value:
            return node

        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def delete(self, value: Any) -> bool:
        """
        Delete a value from the AVL tree maintaining balance.

        Args:
            value: The value to delete

        Returns:
            True if value was deleted, False if not found
        """
        if self._search(value) is None:
            return False

        self._root = self._delete_recursive(self._root, value)
        self._size -= 1
        self._notify_visualizer('delete', {
            'data_structure': self,
            'value': value
        })
        return True

    def _delete_recursive(self, node: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
        """
        Recursive helper for delete with balancing.

        Args:
            node: Current node
            value: Value to delete

        Returns:
            Updated node
        """
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node to delete found
            # Case 1: Node has no children
            if node.left is None and node.right is None:
                return None
            # Case 2: Node has one child
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Case 3: Node has two children
            else:
                # Find inorder successor (smallest in right subtree)
                successor = self._find_min(node.right)
                node.value = successor.value
                node.right = self._delete_recursive(node.right, successor.value)

        # Update balance factor
        balance = self._balance_factor(node)

        # Left Left Case
        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)

        # Left Right Case
        if balance > 1 and self._balance_factor(node.left) < 0:
            return self._rotate_left_right(node)

        # Right Right Case
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)

        # Right Left Case
        if balance < -1 and self._balance_factor(node.right) > 0:
            return self._rotate_right_left(node)

        return node

    def _find_min(self, node: TreeNode) -> TreeNode:
        """Find the node with minimum value."""
        while node.left is not None:
            node = node.left
        return node

    def inorder_traversal(self) -> List[Any]:
        """
        Perform in-order traversal (left, root, right) - gives sorted order.

        Returns:
            List of values in sorted order
        """
        result = []
        self._inorder_recursive(self._root, result)
        return result

    def _inorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """Recursive helper for in-order traversal."""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def _get_internal_state(self) -> Any:
        """
        Get the internal state representation.

        Returns:
            Dictionary representation of the tree with balance factors
        """
        def serialize(node: Optional[TreeNode]) -> Any:
            if node is None:
                return None
            return {
                'value': node.value,
                'balance_factor': self._balance_factor(node),
                'height': self._height(node),
                'left': serialize(node.left),
                'right': serialize(node.right)
            }

        return serialize(self._root)

    def __len__(self) -> int:
        """Return the size of the tree."""
        return self._size

    def __repr__(self) -> str:
        """String representation of the tree."""
        return f"AVLTree(size={self._size})"

