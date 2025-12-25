"""
Data Structure Visualizer
Provides visualizations for data structures with step-by-step and interactive modes.
"""

from typing import Any, Dict, Optional

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
        self._axes.set_xlim(-1, max(len(self._current_state["data"]), 10))
        self._axes.set_ylim(-0.5, 2)
        self._axes.set_aspect("equal")
        self._axes.axis("off")

        # Visualize based on data structure type
        ds_type = self._current_state["type"]

        if ds_type == "Array":
            self._visualize_array(data_structure)
        elif ds_type == "LinkedList":
            self._visualize_linked_list(data_structure)
        elif ds_type == "Stack":
            self._visualize_stack(data_structure)
        elif ds_type == "Queue":
            self._visualize_queue(data_structure)

        # Add title
        title = f"{ds_type} Visualization"
        if step:
            title += f" - Step {step.get('step_number', 'N/A')}"
        self._axes.set_title(title, fontsize=14, fontweight="bold")

        import matplotlib.pyplot as plt

        plt.tight_layout()

    def _visualize_array(self, data_structure: BaseDataStructure):
        """Visualize an array."""
        import matplotlib.patches as patches

        data = self._current_state["data"] if self._current_state is not None else []

        for i, value in enumerate(data):
            # Draw rectangle for each element
            rect = patches.Rectangle(
                (i - 0.4, 0.5),
                0.8,
                1,
                linewidth=2,
                edgecolor="black",
                facecolor="lightblue",
            )
            self._axes.add_patch(rect)

            # Add value text
            self._axes.text(i, 1, str(value), ha="center", va="center", fontsize=12)

            # Add index text
            self._axes.text(
                i, 0.2, str(i), ha="center", va="center", fontsize=10, color="gray"
            )

    def _visualize_linked_list(self, data_structure: BaseDataStructure):
        """Visualize a linked list."""
        import matplotlib.patches as patches

        data = self._current_state["data"] if self._current_state is not None else []

        if not data:
            self._axes.text(0, 1, "Empty List", ha="center", va="center", fontsize=12)
            return

        x_pos = 0
        for i, value in enumerate(data):
            # Draw node circle
            circle = patches.Circle(
                (x_pos, 1), 0.3, linewidth=2, edgecolor="black", facecolor="lightgreen"
            )
            self._axes.add_patch(circle)

            # Add value text
            self._axes.text(x_pos, 1, str(value), ha="center", va="center", fontsize=10)

            # Draw arrow to next node (if not last)
            if i < len(data) - 1:
                self._axes.annotate(
                    "",
                    xy=(x_pos + 0.6, 1),
                    xytext=(x_pos + 0.3, 1),
                    arrowprops=dict(arrowstyle="->", lw=2, color="black"),
                )

            x_pos += 1.2

        # Draw NULL pointer at the end
        self._axes.text(
            x_pos - 0.3, 1, "NULL", ha="left", va="center", fontsize=10, style="italic"
        )

    def _visualize_stack(self, data_structure: BaseDataStructure):
        """Visualize a stack."""
        data = self._current_state["data"] if self._current_state is not None else []

        if not data:
            self._axes.text(0, 1, "Empty Stack", ha="center", va="center", fontsize=12)
            return

        # Draw stack elements from bottom to top
        for i, value in enumerate(data):
            y_pos = i * 0.5
            rect = patches.Rectangle(
                (-0.4, y_pos),
                0.8,
                0.4,
                linewidth=2,
                edgecolor="black",
                facecolor="lightcoral",
            )
            self._axes.add_patch(rect)
            self._axes.text(
                0, y_pos + 0.2, str(value), ha="center", va="center", fontsize=11
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

    def _visualize_queue(self, data_structure: BaseDataStructure):
        """Visualize a queue."""
        import matplotlib.patches as patches

        data = self._current_state["data"] if self._current_state is not None else []

        if not data:
            self._axes.text(0, 1, "Empty Queue", ha="center", va="center", fontsize=12)
            return

        # Draw queue elements from front to rear
        for i, value in enumerate(data):
            rect = patches.Rectangle(
                (i - 0.4, 0.5),
                0.8,
                1,
                linewidth=2,
                edgecolor="black",
                facecolor="lightyellow",
            )
            self._axes.add_patch(rect)
            self._axes.text(i, 1, str(value), ha="center", va="center", fontsize=11)

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
