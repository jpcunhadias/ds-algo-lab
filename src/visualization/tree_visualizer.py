"""
Tree Visualizer
Provides hierarchical tree visualizations with operation highlighting and traversal animations.
"""

from typing import Any, Dict, List, Optional, Tuple
from .base import BaseDataStructure, BaseVisualizer


class TreeVisualizer(BaseVisualizer):
    """
    Visualizer for binary trees (Binary Tree, BST, AVL Tree).
    Provides hierarchical layout and operation visualization.
    """

    def __init__(self):
        """Initialize the tree visualizer."""
        super().__init__()
        self._node_positions: Dict[Any, Tuple[float, float]] = {}
        self._node_radius = 0.3
        self._level_height = 1.5
        self._min_node_spacing = 1.5

    def visualize(
        self,
        data_structure: BaseDataStructure,
        step: Optional[Dict[str, Any]] = None,
        ax=None,
        fig=None,
    ):
        """
        Visualize a tree data structure.

        Args:
            data_structure: The tree to visualize
            step: Optional step information for operation visualization
            ax: Optional matplotlib axes
            fig: Optional matplotlib figure
        """
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches

        if ax is not None:
            self._axes = ax
            self._figure = fig
            self._axes.clear()
        else:
            self._figure, self._axes = plt.subplots(figsize=(14, 10))

        state = data_structure.get_state()
        tree_data = state.get("data")

        if tree_data is None:
            self._axes.text(
                0, 0, "Empty Tree", ha="center", va="center", fontsize=14, fontweight="bold"
            )
            self._axes.axis("off")
            return

        # Calculate node positions
        root = self._deserialize_tree(tree_data)
        if root is None:
            self._axes.text(
                0, 0, "Empty Tree", ha="center", va="center", fontsize=14, fontweight="bold"
            )
            self._axes.axis("off")
            return

        # Calculate layout
        self._calculate_layout(root)

        # Get operation info from step
        operation_type = step.get("operation", "normal") if step else "normal"
        highlighted_nodes = step.get("highlighted_nodes", []) if step else []
        current_node = step.get("current_node", None) if step else None
        traversal_path = step.get("traversal_path", []) if step else []
        rotation_info = step.get("rotation", None) if step else None

        # Draw edges first (so they appear behind nodes)
        self._draw_edges(root, highlighted_nodes, traversal_path)

        # Draw nodes
        self._draw_nodes(
            root,
            highlighted_nodes,
            current_node,
            traversal_path,
            rotation_info,
            data_structure,
        )

        # Set appropriate axis limits
        if self._node_positions:
            x_coords = [pos[0] for pos in self._node_positions.values()]
            y_coords = [pos[1] for pos in self._node_positions.values()]
            x_margin = max(2, max(x_coords) * 0.1) if x_coords else 2
            y_margin = max(1, max(y_coords) * 0.1) if y_coords else 1

            self._axes.set_xlim(min(x_coords) - x_margin, max(x_coords) + x_margin)
            self._axes.set_ylim(min(y_coords) - y_margin, max(y_coords) + y_margin)
        else:
            self._axes.set_xlim(-2, 2)
            self._axes.set_ylim(-1, 3)

        self._axes.set_aspect("equal")
        self._axes.axis("off")

        # Add title
        ds_type = state.get("type", "Tree")
        title = f"{ds_type} Visualization"
        if step:
            if "operation" in step:
                title += f" - {step['operation'].title()}"
            if "step_number" in step:
                title += f" (Step {step['step_number']})"
        self._axes.set_title(title, fontsize=14, fontweight="bold", pad=20)

    def _deserialize_tree(self, tree_data: Any) -> Optional[Any]:
        """
        Deserialize tree from internal state representation.

        Args:
            tree_data: Tree data from get_state()

        Returns:
            Root node or None
        """
        if tree_data is None:
            return None

        # Handle dictionary representation
        if isinstance(tree_data, dict):
            if "value" not in tree_data:
                return None

            # Create a simple node-like structure
            class Node:
                def __init__(self, value):
                    self.value = value
                    self.left = None
                    self.right = None

            def build_node(data):
                if data is None:
                    return None
                node = Node(data["value"])
                node.left = build_node(data.get("left"))
                node.right = build_node(data.get("right"))
                return node

            return build_node(tree_data)

        return None

    def _calculate_layout(self, root: Any) -> None:
        """
        Calculate positions for all nodes using hierarchical layout.

        Args:
            root: Root node of the tree
        """
        self._node_positions.clear()

        if root is None:
            return

        # Calculate subtree widths
        def get_subtree_width(node: Any) -> int:
            """Get width of subtree (number of nodes)."""
            if node is None:
                return 0
            return 1 + get_subtree_width(node.left) + get_subtree_width(node.right)

        def assign_positions(node: Any, x: float, y: float, level: int) -> float:
            """
            Assign positions to nodes recursively.

            Returns:
                Next available x position
            """
            if node is None:
                return x

            # Position current node
            self._node_positions[node.value] = (x, y)

            # Calculate spacing for children
            left_width = get_subtree_width(node.left)
            right_width = get_subtree_width(node.right)

            # Position left subtree
            if node.left is not None:
                left_x = x - (right_width + 1) * self._min_node_spacing / 2
                x = assign_positions(node.left, left_x, y - self._level_height, level + 1)

            # Position right subtree
            if node.right is not None:
                right_x = x + self._min_node_spacing
                x = assign_positions(node.right, right_x, y - self._level_height, level + 1)

            return x

        # Start from root
        root_x = 0
        root_y = 0
        assign_positions(root, root_x, root_y, 0)

    def _draw_edges(
        self, root: Any, highlighted_nodes: List[Any], traversal_path: List[Any]
    ) -> None:
        """
        Draw edges connecting parent and child nodes.

        Args:
            root: Root node
            highlighted_nodes: List of node values to highlight
            traversal_path: List of nodes in traversal order
        """
        if root is None:
            return

        def draw_edge_to_child(parent: Any, child: Any, is_left: bool) -> None:
            """Draw edge from parent to child."""
            if parent is None or child is None:
                return

            parent_pos = self._node_positions.get(parent.value)
            child_pos = self._node_positions.get(child.value)

            if parent_pos is None or child_pos is None:
                return

            px, py = parent_pos
            cx, cy = child_pos

            # Adjust for node radius
            dx = cx - px
            dy = cy - py
            dist = (dx**2 + dy**2) ** 0.5
            if dist > 0:
                # Unit vector
                ux = dx / dist
                uy = dy / dist
                # Start from edge of parent circle
                start_x = px + ux * self._node_radius
                start_y = py + uy * self._node_radius
                # End at edge of child circle
                end_x = cx - ux * self._node_radius
                end_y = cy - uy * self._node_radius

                # Determine edge color
                edge_color = "black"
                edge_width = 1.5
                if child.value in highlighted_nodes:
                    edge_color = "orange"
                    edge_width = 2.5
                elif child.value in traversal_path:
                    edge_color = "blue"
                    edge_width = 2

                self._axes.plot(
                    [start_x, end_x], [start_y, end_y], color=edge_color, linewidth=edge_width
                )

        # Recursively draw edges
        def traverse(node: Any):
            if node is None:
                return
            if node.left is not None:
                draw_edge_to_child(node, node.left, True)
                traverse(node.left)
            if node.right is not None:
                draw_edge_to_child(node, node.right, False)
                traverse(node.right)

        traverse(root)

    def _draw_nodes(
        self,
        root: Any,
        highlighted_nodes: List[Any],
        current_node: Any,
        traversal_path: List[Any],
        rotation_info: Optional[Dict[str, Any]],
        data_structure: BaseDataStructure,
    ) -> None:
        """
        Draw tree nodes with appropriate colors.

        Args:
            root: Root node
            highlighted_nodes: Nodes to highlight
            current_node: Currently active node
            traversal_path: Nodes in traversal order
            rotation_info: Rotation information for AVL trees
            data_structure: The data structure (for balance factors)
        """
        import matplotlib.patches as patches

        def draw_node(node: Any):
            """Draw a single node."""
            if node is None:
                return

            pos = self._node_positions.get(node.value)
            if pos is None:
                return

            x, y = pos

            # Determine node color
            color = "lightgreen"  # Default
            edge_color = "black"
            edge_width = 2

            if node.value == current_node:
                color = "yellow"  # Currently processing
                edge_color = "red"
                edge_width = 3
            elif node.value in highlighted_nodes:
                color = "orange"  # Highlighted
                edge_color = "darkorange"
                edge_width = 2.5
            elif node.value in traversal_path:
                color = "lightblue"  # In traversal path
                edge_color = "blue"
                edge_width = 2
            elif rotation_info:
                # Check if node is involved in rotation
                pivot = rotation_info.get("pivot")
                if node.value == pivot:
                    color = "purple"
                    edge_color = "darkviolet"
                    edge_width = 3

            # Draw node circle
            circle = patches.Circle(
                (x, y),
                self._node_radius,
                linewidth=edge_width,
                edgecolor=edge_color,
                facecolor=color,
            )
            self._axes.add_patch(circle)

            # Add value text
            self._axes.text(
                x,
                y,
                str(node.value),
                ha="center",
                va="center",
                fontsize=11,
                fontweight="bold",
            )

            # Add balance factor for AVL trees
            if hasattr(data_structure, "_balance_factor"):
                try:
                    # Try to get balance factor if it's an AVL tree
                    from ..data_structures.avl_tree import AVLTree

                    if isinstance(data_structure, AVLTree):
                        # Find the node in the tree to get balance factor
                        node_obj = self._find_node_in_tree(data_structure._root, node.value)
                        if node_obj:
                            balance = data_structure._balance_factor(node_obj)
                            self._axes.text(
                                x,
                                y - self._node_radius - 0.15,
                                f"BF:{balance}",
                                ha="center",
                                va="top",
                                fontsize=8,
                                color="gray",
                            )
                except (AttributeError, ImportError):
                    pass

        # Traverse and draw all nodes
        def traverse(node: Any):
            if node is None:
                return
            draw_node(node)
            traverse(node.left)
            traverse(node.right)

        traverse(root)

    def _find_node_in_tree(self, root: Any, value: Any) -> Optional[Any]:
        """Find a node with given value in the tree."""
        if root is None:
            return None
        if root.value == value:
            return root
        left = self._find_node_in_tree(root.left, value)
        if left:
            return left
        return self._find_node_in_tree(root.right, value)

    def visualize_insert(self, data_structure: BaseDataStructure, value: Any, path: List[Any]):
        """
        Visualize insertion operation.

        Args:
            data_structure: The tree
            value: Value being inserted
            path: Path taken during insertion
        """
        step = {
            "operation": "insert",
            "current_node": value,
            "highlighted_nodes": path,
            "description": f"Inserting {value}",
        }
        self.visualize(data_structure, step)

    def visualize_delete(
        self, data_structure: BaseDataStructure, value: Any, path: List[Any]
    ):
        """
        Visualize deletion operation.

        Args:
            data_structure: The tree
            value: Value being deleted
            path: Path taken during deletion
        """
        step = {
            "operation": "delete",
            "current_node": value,
            "highlighted_nodes": path,
            "description": f"Deleting {value}",
        }
        self.visualize(data_structure, step)

    def visualize_search(self, data_structure: BaseDataStructure, value: Any, path: List[Any]):
        """
        Visualize search operation.

        Args:
            data_structure: The tree
            value: Value being searched
            path: Path taken during search
        """
        step = {
            "operation": "search",
            "current_node": value if value in path else None,
            "highlighted_nodes": path,
            "description": f"Searching for {value}",
        }
        self.visualize(data_structure, step)

    def visualize_traversal(
        self,
        data_structure: BaseDataStructure,
        traversal_type: str,
        traversal_order: List[Any],
    ):
        """
        Visualize tree traversal.

        Args:
            data_structure: The tree
            traversal_type: Type of traversal (inorder, preorder, postorder, levelorder)
            traversal_order: Order of nodes in traversal
        """
        step = {
            "operation": f"traversal_{traversal_type}",
            "traversal_path": traversal_order,
            "description": f"{traversal_type.title()} Traversal",
        }
        self.visualize(data_structure, step)

    def visualize_rotation(
        self,
        data_structure: BaseDataStructure,
        rotation_type: str,
        pivot_value: Any,
        new_root_value: Any,
    ):
        """
        Visualize AVL tree rotation.

        Args:
            data_structure: The tree
            rotation_type: Type of rotation (left, right, left_right, right_left)
            pivot_value: Value of pivot node
            new_root_value: Value of new root after rotation
        """
        step = {
            "operation": "rotation",
            "rotation": {
                "type": rotation_type,
                "pivot": pivot_value,
                "new_root": new_root_value,
            },
            "highlighted_nodes": [pivot_value, new_root_value],
            "description": f"{rotation_type.replace('_', ' ').title()} Rotation",
        }
        self.visualize(data_structure, step)

    def animate(self, steps: List[Dict[str, Any]]):
        """
        Animate through a series of tree operation steps.

        Args:
            steps: List of step dictionaries
        """
        import matplotlib.animation as animation
        import matplotlib.pyplot as plt

        if not steps:
            return

        fig, ax = plt.subplots(figsize=(14, 10))

        def animate_frame(frame):
            ax.clear()
            step = steps[frame]
            data_structure = step.get("data_structure")
            if data_structure:
                self.visualize(data_structure, step, ax=ax, fig=fig)

        _ = animation.FuncAnimation(
            fig, animate_frame, frames=len(steps), interval=1000, repeat=False
        )

        plt.tight_layout()
        plt.show()

