"""
Binary Search Tree (BST) data structure implementation.
A BST with visualization hooks.
"""

from typing import Any, Optional, List
from .binary_tree import TreeNode
from ..visualization.base import BaseDataStructure


class BinarySearchTree(BaseDataStructure):
    """
    Binary Search Tree implementation with visualization support.
    Maintains BST property: left < root < right
    """

    def __init__(self, initial_data: Optional[List[Any]] = None):
        """
        Initialize the binary search tree.

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

    def insert(self, value: Any) -> None:
        """
        Insert a value into the BST maintaining BST property.

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
        Recursive helper for insert.

        Args:
            node: Current node
            value: Value to insert

        Returns:
            Updated node
        """
        if node is None:
            return TreeNode(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        # If value == node.value, we don't insert duplicates (or could allow based on requirement)

        return node

    def search(self, value: Any) -> Optional[TreeNode]:
        """
        Search for a value in the BST.

        Args:
            value: The value to search for

        Returns:
            The node containing the value, or None if not found
        """
        node = self._search_recursive(self._root, value)
        self._notify_visualizer('search', {
            'data_structure': self,
            'value': value,
            'found': node is not None
        })
        return node

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
        Delete a value from the BST.

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
        Recursive helper for delete.

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

        return node

    def find_min(self) -> Optional[Any]:
        """
        Find the minimum value in the BST.

        Returns:
            Minimum value or None if tree is empty
        """
        if self._root is None:
            return None
        return self._find_min(self._root).value

    def _find_min(self, node: TreeNode) -> TreeNode:
        """Find the node with minimum value."""
        while node.left is not None:
            node = node.left
        return node

    def find_max(self) -> Optional[Any]:
        """
        Find the maximum value in the BST.

        Returns:
            Maximum value or None if tree is empty
        """
        if self._root is None:
            return None
        return self._find_max(self._root).value

    def _find_max(self, node: TreeNode) -> TreeNode:
        """Find the node with maximum value."""
        while node.right is not None:
            node = node.right
        return node

    def successor(self, value: Any) -> Optional[Any]:
        """
        Find the successor of a value (next larger value).

        Args:
            value: The value to find successor for

        Returns:
            Successor value or None if not found
        """
        node = self._search_recursive(self._root, value)
        if node is None:
            return None

        if node.right is not None:
            return self._find_min(node.right).value

        # Find the lowest ancestor whose left child is an ancestor of node
        successor = None
        current = self._root
        while current is not None:
            if value < current.value:
                successor = current
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                break

        return successor.value if successor else None

    def predecessor(self, value: Any) -> Optional[Any]:
        """
        Find the predecessor of a value (next smaller value).

        Args:
            value: The value to find predecessor for

        Returns:
            Predecessor value or None if not found
        """
        node = self._search_recursive(self._root, value)
        if node is None:
            return None

        if node.left is not None:
            return self._find_max(node.left).value

        # Find the lowest ancestor whose right child is an ancestor of node
        predecessor = None
        current = self._root
        while current is not None:
            if value > current.value:
                predecessor = current
                current = current.right
            elif value < current.value:
                current = current.left
            else:
                break

        return predecessor.value if predecessor else None

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

    def preorder_traversal(self) -> List[Any]:
        """
        Perform pre-order traversal (root, left, right).

        Returns:
            List of values in pre-order
        """
        result = []
        self._preorder_recursive(self._root, result)
        return result

    def _preorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """Recursive helper for pre-order traversal."""
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder_traversal(self) -> List[Any]:
        """
        Perform post-order traversal (left, right, root).

        Returns:
            List of values in post-order
        """
        result = []
        self._postorder_recursive(self._root, result)
        return result

    def _postorder_recursive(self, node: Optional[TreeNode], result: List[Any]) -> None:
        """Recursive helper for post-order traversal."""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

    def _get_internal_state(self) -> Any:
        """
        Get the internal state representation.

        Returns:
            Dictionary representation of the tree
        """
        def serialize(node: Optional[TreeNode]) -> Any:
            if node is None:
                return None
            return {
                'value': node.value,
                'left': serialize(node.left),
                'right': serialize(node.right)
            }

        return serialize(self._root)

    def __len__(self) -> int:
        """Return the size of the tree."""
        return self._size

    def __repr__(self) -> str:
        """String representation of the tree."""
        return f"BinarySearchTree(size={self._size})"

