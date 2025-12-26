"""
Data Structure Visualizer
Provides visualizations for data structures with step-by-step and interactive modes.
"""

from typing import Any, Dict, List, Optional

from .base import BaseDataStructure, BaseVisualizer


class DataStructureVisualizer(BaseVisualizer):
    """
    Visualizer for data structures with step-by-step and interactive modes.
    """

    def __init__(self):
        """Initialize the data structure visualizer."""
        super().__init__()
        self._current_state = None

    def visualize(
        self, data_structure: BaseDataStructure, step: Optional[Dict[str, Any]] = None
    ):
        """
        Visualize the current state of a data structure.

        Args:
            data_structure: The data structure to visualize
            step: Optional step information (for algorithm visualization)
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print(
                "matplotlib is required for visualization. Install it with: pip install matplotlib"
            )
            return

        self._current_state = data_structure.get_state()

        # Create figure and axis
        self._figure, self._axes = plt.subplots(figsize=(10, 6))
        self._axes.set_xlim(-1, max(len(self._current_state.get("data", [])), 10))
        self._axes.set_ylim(-0.5, 2)
        self._axes.set_aspect("equal")
        self._axes.axis("off")

        # Visualize based on data structure type
        ds_type = self._current_state["type"]

        # Extract operation info from step
        operation = step.get("operation", "normal") if step else "normal"
        current_index = step.get("current_index", None) if step else None
        highlighted_indices = step.get("highlighted_indices", []) if step else []

        if ds_type == "Array":
            self._visualize_array(data_structure, current_index, highlighted_indices)
        elif ds_type == "LinkedList":
            self._visualize_linked_list(
                data_structure, current_index, highlighted_indices
            )
        elif ds_type == "Stack":
            self._visualize_stack(data_structure, current_index, highlighted_indices)
        elif ds_type == "Queue":
            self._visualize_queue(data_structure, current_index, highlighted_indices)
        elif ds_type in ["BinaryTree", "BinarySearchTree", "AVLTree"]:
            # Use tree visualizer for better visualization
            from .tree_visualizer import TreeVisualizer

            tree_viz = TreeVisualizer()
            tree_viz.visualize(data_structure, step, ax=self._axes, fig=self._figure)
            return
        elif ds_type == "Graph":
            # Use graph visualizer for better visualization
            from .graph_visualizer import GraphVisualizer

            graph_viz = GraphVisualizer()
            graph_viz.visualize(data_structure, step, ax=self._axes, fig=self._figure)
            return
        elif ds_type == "HashTable":
            # Use hash table visualizer for better visualization
            from .hash_table_visualizer import HashTableVisualizer

            ht_viz = HashTableVisualizer()
            ht_viz.visualize(data_structure, step, ax=self._axes, fig=self._figure)
            return

        # Add title
        title = f"{ds_type} Visualization"
        if step:
            if "operation" in step:
                title += f" - {step['operation'].title()}"
            if "step_number" in step:
                title += f" (Step {step['step_number']})"
        self._axes.set_title(title, fontsize=14, fontweight="bold")

        import matplotlib.pyplot as plt

        plt.tight_layout()

    def _visualize_array(
        self,
        data_structure: BaseDataStructure,
        current_index: Optional[int] = None,
        highlighted_indices: List[int] = None,
    ):
        """Visualize an array with operation highlighting."""
        import matplotlib.patches as patches

        if highlighted_indices is None:
            highlighted_indices = []

        data = self._current_state["data"] if self._current_state is not None else []

        for i, value in enumerate(data):
            # Determine color based on operation state
            color = "lightblue"  # Default
            edge_color = "black"
            edge_width = 2

            if i == current_index:
                color = "yellow"  # Currently processing
                edge_color = "red"
                edge_width = 3
            elif i in highlighted_indices:
                color = "orange"  # Highlighted
                edge_color = "darkorange"
                edge_width = 2.5

            # Draw rectangle for each element
            rect = patches.Rectangle(
                (i - 0.4, 0.5),
                0.8,
                1,
                linewidth=edge_width,
                edgecolor=edge_color,
                facecolor=color,
            )
            self._axes.add_patch(rect)

            # Add value text
            self._axes.text(
                i,
                1,
                str(value),
                ha="center",
                va="center",
                fontsize=12,
                fontweight="bold",
            )

            # Add index text
            self._axes.text(
                i, 0.2, str(i), ha="center", va="center", fontsize=10, color="gray"
            )

    def _visualize_linked_list(
        self,
        data_structure: BaseDataStructure,
        current_index: Optional[int] = None,
        highlighted_indices: List[int] = None,
    ):
        """Visualize a linked list with operation highlighting."""
        import matplotlib.patches as patches

        if highlighted_indices is None:
            highlighted_indices = []

        data = self._current_state["data"] if self._current_state is not None else []

        if not data:
            self._axes.text(0, 1, "Empty List", ha="center", va="center", fontsize=12)
            return

        x_pos = 0
        for i, value in enumerate(data):
            # Determine color based on operation state
            color = "lightgreen"  # Default
            edge_color = "black"
            edge_width = 2

            if i == current_index:
                color = "yellow"  # Currently processing
                edge_color = "red"
                edge_width = 3
            elif i in highlighted_indices:
                color = "orange"  # Highlighted
                edge_color = "darkorange"
                edge_width = 2.5

            # Draw node circle
            circle = patches.Circle(
                (x_pos, 1),
                0.3,
                linewidth=edge_width,
                edgecolor=edge_color,
                facecolor=color,
            )
            self._axes.add_patch(circle)

            # Add value text
            self._axes.text(
                x_pos,
                1,
                str(value),
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

            # Draw arrow to next node (if not last)
            if i < len(data) - 1:
                arrow_color = "black"
                arrow_width = 2
                if i in highlighted_indices or (i + 1) in highlighted_indices:
                    arrow_color = "orange"
                    arrow_width = 2.5

                self._axes.annotate(
                    "",
                    xy=(x_pos + 0.6, 1),
                    xytext=(x_pos + 0.3, 1),
                    arrowprops=dict(arrowstyle="->", lw=arrow_width, color=arrow_color),
                )

            x_pos += 1.2

        # Draw NULL pointer at the end
        self._axes.text(
            x_pos - 0.3, 1, "NULL", ha="left", va="center", fontsize=10, style="italic"
        )

    def _visualize_stack(
        self,
        data_structure: BaseDataStructure,
        current_index: Optional[int] = None,
        highlighted_indices: List[int] = None,
    ):
        """Visualize a stack with operation highlighting."""
        import matplotlib.patches as patches

        if highlighted_indices is None:
            highlighted_indices = []

        data = self._current_state["data"] if self._current_state is not None else []

        if not data:
            self._axes.text(0, 1, "Empty Stack", ha="center", va="center", fontsize=12)
            return

        # Draw stack elements from bottom to top
        for i, value in enumerate(data):
            y_pos = i * 0.5

            # Determine color based on operation state
            color = "lightcoral"  # Default
            edge_color = "black"
            edge_width = 2

            if i == current_index:
                color = "yellow"  # Currently processing
                edge_color = "red"
                edge_width = 3
            elif i in highlighted_indices:
                color = "orange"  # Highlighted
                edge_color = "darkorange"
                edge_width = 2.5
            elif i == len(data) - 1:
                # Top element
                color = "lightcoral"
                edge_color = "red"
                edge_width = 2.5

            rect = patches.Rectangle(
                (-0.4, y_pos),
                0.8,
                0.4,
                linewidth=edge_width,
                edgecolor=edge_color,
                facecolor=color,
            )
            self._axes.add_patch(rect)
            self._axes.text(
                0,
                y_pos + 0.2,
                str(value),
                ha="center",
                va="center",
                fontsize=11,
                fontweight="bold",
            )

        # Add "TOP" label
        if data:
            self._axes.text(
                0.6,
                (len(data) - 1) * 0.5 + 0.2,
                "TOP",
                ha="left",
                va="center",
                fontsize=10,
                fontweight="bold",
                color="red",
            )

    def _visualize_queue(
        self,
        data_structure: BaseDataStructure,
        current_index: Optional[int] = None,
        highlighted_indices: List[int] = None,
    ):
        """Visualize a queue with operation highlighting."""
        import matplotlib.patches as patches

        if highlighted_indices is None:
            highlighted_indices = []

        data = self._current_state["data"] if self._current_state is not None else []

        if not data:
            self._axes.text(0, 1, "Empty Queue", ha="center", va="center", fontsize=12)
            return

        # Draw queue elements from front to rear
        for i, value in enumerate(data):
            # Determine color based on operation state
            color = "lightyellow"  # Default
            edge_color = "black"
            edge_width = 2

            if i == current_index:
                color = "yellow"  # Currently processing
                edge_color = "red"
                edge_width = 3
            elif i in highlighted_indices:
                color = "orange"  # Highlighted
                edge_color = "darkorange"
                edge_width = 2.5
            elif i == 0:
                # Front element
                color = "lightgreen"
                edge_color = "green"
                edge_width = 2.5
            elif i == len(data) - 1:
                # Rear element
                color = "lightblue"
                edge_color = "blue"
                edge_width = 2.5

            rect = patches.Rectangle(
                (i - 0.4, 0.5),
                0.8,
                1,
                linewidth=edge_width,
                edgecolor=edge_color,
                facecolor=color,
            )
            self._axes.add_patch(rect)
            self._axes.text(
                i,
                1,
                str(value),
                ha="center",
                va="center",
                fontsize=11,
                fontweight="bold",
            )

        # Add FRONT and REAR labels
        if data:
            self._axes.text(
                0,
                0.2,
                "FRONT",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                color="green",
            )
            self._axes.text(
                len(data) - 1,
                0.2,
                "REAR",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                color="blue",
            )

    def animate(self, steps: list):
        """
        Animate through a series of steps.

        Args:
            steps: List of step dictionaries to animate
        """
        import matplotlib.pyplot as plt

        for i, step in enumerate(steps):
            if "data_structure" in step:
                self.visualize(step["data_structure"], {"step_number": i + 1})
                plt.pause(0.5)  # Pause between steps
                plt.clf()

    def _visualize_tree(self, data_structure: BaseDataStructure):
        """Visualize a binary tree."""
        import matplotlib.patches as patches

        data = self._current_state["data"] if self._current_state is not None else []

        if not data:
            self._axes.text(0, 0, "Empty Tree", ha="center", va="center", fontsize=12)
            return

        # Adjust axes for tree visualization
        self._axes.set_xlim(-2, max(len(data) * 2, 10))
        self._axes.set_ylim(-1, 5)

        # Simple tree visualization - level order representation
        # For a more sophisticated visualization, we'd need tree structure
        y_levels = [4, 3, 2, 1, 0]
        x_positions = {}

        # Calculate positions (simplified - assumes complete tree)
        level = 0
        x = 0

        for i, value in enumerate(data):
            if value is None:
                continue

            # Calculate position
            if i == 0:
                x = 0
            else:
                # Simple positioning
                parent_idx = (i - 1) // 2
                is_left = i % 2 == 1
                if parent_idx in x_positions:
                    parent_x = x_positions[parent_idx][0]
                    spacing = 2 / (2**level)
                    x = parent_x - spacing if is_left else parent_x + spacing

            y = y_levels[min(level, len(y_levels) - 1)]
            x_positions[i] = (x, y)

            # Draw node
            circle = patches.Circle(
                (x, y), 0.3, linewidth=2, edgecolor="black", facecolor="lightgreen"
            )
            self._axes.add_patch(circle)
            self._axes.text(x, y, str(value), ha="center", va="center", fontsize=10)

            # Draw connection to parent
            if i > 0:
                parent_idx = (i - 1) // 2
                if parent_idx in x_positions:
                    px, py = x_positions[parent_idx]
                    self._axes.plot([px, x], [py - 0.3, y + 0.3], "k-", linewidth=1)

            # Move to next level if needed
            if i + 1 >= 2 ** (level + 1) - 1:
                level += 1

    def _visualize_graph(self, data_structure: BaseDataStructure):
        """Visualize a graph."""
        import math

        import matplotlib.patches as patches

        state = self._current_state if self._current_state is not None else {}
        adjacency_list = state.get("data", {})

        if not adjacency_list:
            self._axes.text(0, 0, "Empty Graph", ha="center", va="center", fontsize=12)
            return

        # Adjust axes
        num_vertices = len(adjacency_list)
        self._axes.set_xlim(-2, num_vertices + 2)
        self._axes.set_ylim(-2, num_vertices + 2)

        # Position vertices in a circle
        vertices = list(adjacency_list.keys())
        positions = {}
        radius = num_vertices / 2 if num_vertices > 1 else 1
        center_x, center_y = num_vertices / 2, num_vertices / 2

        for i, vertex in enumerate(vertices):
            angle = 2 * math.pi * i / num_vertices if num_vertices > 1 else 0
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions[vertex] = (x, y)

        # Draw edges
        for vertex, neighbors in adjacency_list.items():
            if vertex in positions:
                vx, vy = positions[vertex]
                for neighbor in neighbors:
                    if neighbor in positions:
                        nx, ny = positions[neighbor]
                        self._axes.plot(
                            [vx, nx], [vy, ny], "b-", linewidth=1, alpha=0.5
                        )

        # Draw vertices
        for vertex, (x, y) in positions.items():
            circle = patches.Circle(
                (x, y), 0.4, linewidth=2, edgecolor="black", facecolor="lightblue"
            )
            self._axes.add_patch(circle)
            self._axes.text(
                x,
                y,
                str(vertex),
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

    def _visualize_hash_table(self, data_structure: BaseDataStructure):
        """Visualize a hash table."""
        import matplotlib.patches as patches

        state = self._current_state if self._current_state is not None else {}
        items = state.get("data", {})

        if not items:
            self._axes.text(
                0, 0, "Empty Hash Table", ha="center", va="center", fontsize=12
            )
            return

        # Adjust axes
        num_buckets = max(len(items), 8)
        self._axes.set_xlim(-1, num_buckets)
        self._axes.set_ylim(-0.5, 3)

        # Draw buckets
        bucket_width = 0.8
        for i in range(num_buckets):
            x = i
            rect = patches.Rectangle(
                (x - bucket_width / 2, 0),
                bucket_width,
                2,
                linewidth=2,
                edgecolor="black",
                facecolor="lightgray",
            )
            self._axes.add_patch(rect)
            self._axes.text(x, 2.2, f"Bucket {i}", ha="center", va="center", fontsize=9)

        # Place items in buckets (simplified - just show items)
        y_offset = 1.5
        for i, (key, value) in enumerate(items.items()):
            bucket_idx = i % num_buckets
            x = bucket_idx
            y = y_offset - (i // num_buckets) * 0.3

            # Draw key-value pair
            rect = patches.Rectangle(
                (x - bucket_width / 2 + 0.1, y - 0.1),
                bucket_width - 0.2,
                0.2,
                linewidth=1,
                edgecolor="blue",
                facecolor="lightblue",
            )
            self._axes.add_patch(rect)
            self._axes.text(
                x, y, f"{key}:{value}", ha="center", va="center", fontsize=8
            )

    def interactive_mode(self):
        """
        Enter interactive mode for user manipulation.
        This is a basic implementation - can be enhanced with GUI.
        """
        print("Interactive mode - Enter commands:")
        print("Commands: push <value>, pop, peek, quit")

        # This is a placeholder - full interactive mode would require
        # a more sophisticated GUI or command loop
        pass
