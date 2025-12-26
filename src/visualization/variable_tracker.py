"""
Variable Tracker
Displays variable values during algorithm execution.
"""

from typing import Any, Dict, List


class VariableTracker:
    """
    Tracks and displays variable values during algorithm execution.
    """

    def __init__(self):
        """Initialize variable tracker."""
        self.variables: Dict[str, Any] = {}
        self.history: List[Dict[str, Any]] = []

    def update(self, variables: Dict[str, Any]) -> None:
        """
        Update variable values.

        Args:
            variables: Dictionary of variable names to values
        """
        self.variables = variables.copy()
        self.history.append(variables.copy())

    def set_variable(self, name: str, value: Any) -> None:
        """
        Set a single variable value.

        Args:
            name: Variable name
            value: Variable value
        """
        self.variables[name] = value

    def get_variable(self, name: str, default: Any = None) -> Any:
        """
        Get a variable value.

        Args:
            name: Variable name
            default: Default value if not found

        Returns:
            Variable value
        """
        return self.variables.get(name, default)

    def clear(self) -> None:
        """Clear all variables."""
        self.variables = {}
        self.history = []

    def render(
        self,
        ax,
        position: str = "left",
        max_variables: int = 10,
        show_history: bool = False,
    ) -> None:
        """
        Render variable tracker on matplotlib axes.

        Args:
            ax: Matplotlib axes to render on
            position: Position of panel ('left', 'right', 'top', 'bottom')
            max_variables: Maximum number of variables to display
            show_history: Whether to show variable history
        """
        ax.clear()
        ax.axis("off")

        if not self.variables:
            ax.text(
                0.5,
                0.5,
                "No variables tracked",
                ha="center",
                va="center",
                fontsize=10,
                color="gray",
                transform=ax.transAxes,
            )
            return

        # Title
        ax.text(
            0.5,
            0.95,
            "Variables",
            fontsize=12,
            fontweight="bold",
            ha="center",
            transform=ax.transAxes,
        )

        # Draw separator
        ax.plot(
            [0.1, 0.9],
            [0.9, 0.9],
            color="#CCCCCC",
            linewidth=1,
            transform=ax.transAxes,
        )

        # Display variables
        y_start = 0.85
        line_height = 0.75 / min(len(self.variables), max_variables)
        font_size = 9

        sorted_vars = sorted(self.variables.items())[:max_variables]

        for i, (var_name, var_value) in enumerate(sorted_vars):
            y_pos = y_start - i * line_height

            # Format value for display
            display_value = self._format_value(var_value)

            # Variable name
            ax.text(
                0.1,
                y_pos,
                f"{var_name}:",
                fontsize=font_size,
                fontweight="bold",
                fontfamily="monospace",
                transform=ax.transAxes,
                verticalalignment="center",
            )

            # Variable value
            ax.text(
                0.5,
                y_pos,
                str(display_value),
                fontsize=font_size,
                fontfamily="monospace",
                color="#0066CC",
                transform=ax.transAxes,
                verticalalignment="center",
            )

        # Show history if enabled
        if show_history and len(self.history) > 1:
            self._render_history(ax, y_start - len(sorted_vars) * line_height - 0.05)

    def _format_value(self, value: Any) -> str:
        """
        Format value for display.

        Args:
            value: Value to format

        Returns:
            Formatted string
        """
        if isinstance(value, (list, tuple)):
            if len(value) > 5:
                return f"[{', '.join(map(str, value[:3]))}... ({len(value)} items)]"
            return str(value)
        elif isinstance(value, dict):
            # Don't show full tree structure - just indicate it's a tree
            if "value" in value and ("left" in value or "right" in value):
                return f"Tree node (value: {value.get('value', '?')})"
            if len(value) > 3:
                return f"{{...}} ({len(value)} items)"
            return str(value)
        elif isinstance(value, float):
            return f"{value:.2f}"
        elif value is None:
            return "None"
        else:
            return str(value)

    def _render_history(self, ax, y_start: float) -> None:
        """
        Render variable history.

        Args:
            ax: Matplotlib axes
            y_start: Starting y position
        """
        if len(self.history) <= 1:
            return

        # Draw separator
        ax.plot(
            [0.1, 0.9],
            [y_start, y_start],
            color="#CCCCCC",
            linewidth=1,
            transform=ax.transAxes,
        )

        # Show recent changes
        ax.text(
            0.1,
            y_start - 0.03,
            f"History: {len(self.history)} steps",
            fontsize=8,
            color="gray",
            transform=ax.transAxes,
        )

    def extract_from_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract variables from algorithm step.

        Args:
            step: Step dictionary

        Returns:
            Dictionary of extracted variables
        """
        variables = {}

        # Common algorithm variables
        if "current" in step:
            variables["current_index"] = step["current"]
        if "comparing" in step:
            variables["comparing_indices"] = step["comparing"]
        if "swapping" in step:
            variables["swapping_indices"] = step["swapping"]
        if "sorted" in step:
            variables["sorted_count"] = len(step["sorted"])
        if "step_number" in step:
            variables["step"] = step["step_number"]

        # Algorithm-specific variables
        if "pivot" in step:
            variables["pivot"] = step["pivot"]
        if "left" in step and "right" in step:
            variables["left"] = step["left"]
            variables["right"] = step["right"]
        if "mid" in step:
            variables["mid"] = step["mid"]
        if "mid1" in step:
            variables["mid1"] = step["mid1"]
        if "mid2" in step:
            variables["mid2"] = step["mid2"]
        if "target" in step:
            variables["target"] = step["target"]
        if "found_index" in step:
            variables["found_index"] = step["found_index"]

        # Tree-specific variables
        if "operation" in step:
            variables["operation"] = step["operation"]
        if "current_node" in step:
            variables["current_node"] = step["current_node"]
        if "highlighted_nodes" in step:
            highlighted = step["highlighted_nodes"]
            if isinstance(highlighted, list) and len(highlighted) > 0:
                variables["path_length"] = len(highlighted)
                if len(highlighted) <= 5:
                    variables["path"] = highlighted
        if "traversal_path" in step:
            path = step["traversal_path"]
            if isinstance(path, list):
                variables["traversal_length"] = len(path)
                if len(path) <= 5:
                    variables["traversal_path"] = path

        # Data structure state
        data_structure = step.get("data_structure")
        if data_structure:
            state = data_structure.get_state()
            ds_type = state.get("type", "")

            # Handle tree data structures differently
            if ds_type in ["BinaryTree", "BinarySearchTree", "AVLTree"]:
                tree_data = state.get("data")
                if tree_data:
                    # Extract tree size instead of showing entire structure
                    variables["tree_size"] = self._get_tree_size(tree_data)
                    variables["tree_type"] = ds_type
                    # Don't show the entire tree structure - it's too complex
            else:
                # Array-like structures
                data = state.get("data", [])
                if isinstance(data, list):
                    variables["array_length"] = len(data)
                    if len(data) <= 10:  # Only show small arrays
                        variables["array"] = data
                elif isinstance(data, dict):
                    # This might be a tree structure incorrectly stored as "data"
                    # Don't show it as array - check if it looks like a tree node
                    if "value" in data and ("left" in data or "right" in data):
                        # It's a tree structure, not an array
                        variables["tree_size"] = self._get_tree_size(data)
                        variables["tree_type"] = "Tree"
                    # Otherwise skip it

        return variables

    def _get_tree_size(self, tree_data: Any) -> int:
        """
        Get size of tree from tree data structure.

        Args:
            tree_data: Tree data (could be dict, TreeNode, or other format)

        Returns:
            Tree size
        """
        if tree_data is None:
            return 0

        # If it's a dict representation
        if isinstance(tree_data, dict):
            size = 1
            if "left" in tree_data:
                size += self._get_tree_size(tree_data["left"])
            if "right" in tree_data:
                size += self._get_tree_size(tree_data["right"])
            return size

        # If it's a TreeNode-like object
        if hasattr(tree_data, "value"):
            size = 1
            if hasattr(tree_data, "left"):
                size += self._get_tree_size(tree_data.left)
            if hasattr(tree_data, "right"):
                size += self._get_tree_size(tree_data.right)
            return size

        return 0
