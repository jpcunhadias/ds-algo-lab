"""
Binary Tree data structure implementation.
A binary tree with visualization hooks.
"""

from typing import Any, Optional, List
from ..visualization.base import BaseDataStructure


class TreeNode:
    """
    Node class for binary tree.
    """

    def __init__(self, value: Any):
        """
        Initialize a tree node.

        Args:
            value: The value stored in the node
        """
        self.value = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

    def __repr__(self) -> str:
        """String representation of the node."""
        return f"TreeNode({self.value})"


class BinaryTree(BaseDataStructure):
    """
    Binary Tree implementation with visualization support.
    """

    def __init__(self, initial_data: Optional[List[Any]] = None):
        """
        Initialize the binary tree.

        Args:
            initial_data: Optional initial data to populate the tree
        """
        super().__init__()
        self._root: Optional[TreeNode] = None
        self._size = 0

        # Build tree from initial data (level-order insertion)
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
        Insert a value into the binary tree (level-order insertion).

        Args:
            value: The value to insert
        """
        new_node = TreeNode(value)

        if self._root is None:
            self._root = new_node
        else:
            # Level-order insertion using queue
            queue = [self._root]
            while queue:
                node = queue.pop(0)

                if node.left is None:
                    node.left = new_node
                    break
                elif node.right is None:
                    node.right = new_node
                    break
                else:
                    queue.append(node.left)
                    queue.append(node.right)

        self._size += 1
        self._notify_visualizer('insert', {
            'data_structure': self,
            'value': value
        })

    def search(self, value: Any) -> Optional[TreeNode]:
        """
        Search for a value in the binary tree.

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
        if node is None:
            return None

        if node.value == value:
            self._notify_visualizer('search', {
                'data_structure': self,
                'value': value,
                'found': True
            })
            return node

        # Search left subtree
        left_result = self._search_recursive(node.left, value)
        if left_result:
            return left_result

        # Search right subtree
        return self._search_recursive(node.right, value)

    def delete(self, value: Any) -> bool:
        """
        Delete a value from the binary tree.

        Args:
            value: The value to delete

        Returns:
            True if value was deleted, False if not found
        """
        if self._root is None:
            return False

        # Find the node to delete and the deepest node
        node_to_delete = None
        deepest_node = None
        parent_of_deepest = None

        # Find node to delete
        queue = [self._root]
        while queue:
            node = queue.pop(0)
            if node.value == value:
                node_to_delete = node
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        if node_to_delete is None:
            return False

        # Find deepest node (rightmost node at deepest level)
        queue = [self._root]
        while queue:
            node = queue.pop(0)
            deepest_node = node
            if node.left:
                parent_of_deepest = node
                queue.append(node.left)
            if node.right:
                parent_of_deepest = node
                queue.append(node.right)

        # Replace node_to_delete with deepest_node
        if deepest_node and node_to_delete != deepest_node:
            node_to_delete.value = deepest_node.value

            # Remove deepest node
            if parent_of_deepest:
                if parent_of_deepest.left == deepest_node:
                    parent_of_deepest.left = None
                else:
                    parent_of_deepest.right = None
            else:
                # Deepest node is root
                self._root = None

        self._size -= 1
        self._notify_visualizer('delete', {
            'data_structure': self,
            'value': value
        })
        return True

    def inorder_traversal(self) -> List[Any]:
        """
        Perform in-order traversal (left, root, right).

        Returns:
            List of values in in-order
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

    def level_order_traversal(self) -> List[Any]:
        """
        Perform level-order traversal (breadth-first).

        Returns:
            List of values in level-order
        """
        result = []
        if self._root is None:
            return result

        queue = [self._root]
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

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
        return f"BinaryTree(size={self._size})"

