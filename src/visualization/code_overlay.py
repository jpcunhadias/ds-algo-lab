"""
Code Overlay System
Displays algorithm code alongside visualization with current line highlighting.
"""

from typing import Any, Dict, Optional

import matplotlib.patches as patches


class CodeOverlay:
    """
    Displays algorithm code with syntax highlighting and current line indication.
    """

    def __init__(self, code: str, algorithm_name: str = ""):
        """
        Initialize code overlay.

        Args:
            code: Algorithm code as string
            algorithm_name: Name of the algorithm
        """
        self.code = code
        self.algorithm_name = algorithm_name
        self.lines = code.split("\n")
        self.current_line = -1
        self.variables: Dict[str, Any] = {}

    def set_current_line(self, line_number: int) -> None:
        """
        Set the currently executing line.

        Args:
            line_number: Line number (0-indexed)
        """
        self.current_line = line_number

    def set_variables(self, variables: Dict[str, Any]) -> None:
        """
        Set variable values to display.

        Args:
            variables: Dictionary of variable names to values
        """
        self.variables = variables

    def render(
        self,
        ax,
        position: str = "right",
        width_ratio: float = 0.3,
        max_lines: int = 20,
    ) -> None:
        """
        Render code overlay on matplotlib axes.

        Args:
            ax: Matplotlib axes to render on
            position: Position of overlay ('right', 'left', 'bottom')
            width_ratio: Ratio of width/height for code panel
            max_lines: Maximum number of lines to display
        """
        ax.axis("off")

        # Determine visible lines (with scrolling if needed)
        total_lines = len(self.lines)
        if total_lines <= max_lines:
            start_line = 0
            visible_lines = self.lines
        else:
            # Center around current line
            if self.current_line >= 0:
                start_line = max(0, self.current_line - max_lines // 2)
                start_line = min(start_line, total_lines - max_lines)
            else:
                start_line = 0
            visible_lines = self.lines[start_line : start_line + max_lines]

        # Calculate positions
        y_start = 0.95
        line_height = 0.9 / len(visible_lines) if visible_lines else 0.05
        font_size = min(10, max(6, int(12 * line_height * 10)))

        # Draw code lines
        for i, line in enumerate(visible_lines):
            line_num = start_line + i
            y_pos = y_start - i * line_height

            # Highlight current line
            if line_num == self.current_line:
                # Draw background highlight
                rect = patches.Rectangle(
                    (0.02, y_pos - line_height * 0.4),
                    0.96,
                    line_height * 0.8,
                    linewidth=2,
                    edgecolor="#FFA500",  # Orange
                    facecolor="#FFF9C4",  # Light yellow
                    alpha=0.7,
                    transform=ax.transAxes,
                )
                ax.add_patch(rect)

                # Add arrow indicator
                ax.text(
                    0.01,
                    y_pos,
                    "▶",
                    fontsize=font_size,
                    color="#FF6B00",
                    transform=ax.transAxes,
                    verticalalignment="center",
                )

            # Determine text color based on line content
            text_color = self._get_line_color(line)

            # Display line number
            ax.text(
                0.05,
                y_pos,
                f"{line_num + 1:3d}",
                fontsize=font_size - 1,
                color="#666666",
                fontfamily="monospace",
                transform=ax.transAxes,
                verticalalignment="center",
            )

            # Display code line
            ax.text(
                0.12,
                y_pos,
                self._format_code_line(line),
                fontsize=font_size,
                color=text_color,
                fontfamily="monospace",
                transform=ax.transAxes,
                verticalalignment="center",
            )

        # Display variable values if available
        if self.variables:
            self._render_variables(
                ax, y_start - len(visible_lines) * line_height - 0.05
            )

        # Add title
        if self.algorithm_name:
            ax.text(
                0.5,
                0.98,
                f"Algorithm: {self.algorithm_name}",
                fontsize=font_size + 2,
                fontweight="bold",
                ha="center",
                transform=ax.transAxes,
            )

    def _get_line_color(self, line: str) -> str:
        """
        Determine text color based on line content.

        Args:
            line: Code line

        Returns:
            Color string
        """
        line_stripped = line.strip()

        # Keywords
        keywords = [
            "def",
            "if",
            "else",
            "elif",
            "for",
            "while",
            "return",
            "yield",
            "class",
        ]
        if any(line_stripped.startswith(kw) for kw in keywords):
            return "#0000FF"  # Blue

        # Comments
        if line_stripped.startswith("#"):
            return "#008000"  # Green

        # Strings
        if '"' in line or "'" in line:
            return "#800080"  # Purple

        # Default
        return "#000000"  # Black

    def _format_code_line(self, line: str) -> str:
        """
        Format code line for display (handle long lines).

        Args:
            line: Code line

        Returns:
            Formatted line
        """
        # Truncate very long lines
        max_length = 60
        if len(line) > max_length:
            return line[:max_length] + "..."
        return line

    def _render_variables(self, ax, y_start: float) -> None:
        """
        Render variable values below code.

        Args:
            ax: Matplotlib axes
            y_start: Starting y position
        """
        if not self.variables:
            return

        # Draw separator
        ax.plot(
            [0.05, 0.95],
            [y_start, y_start],
            color="#CCCCCC",
            linewidth=1,
            transform=ax.transAxes,
        )

        # Display variables
        y_pos = y_start - 0.03
        ax.text(
            0.05,
            y_pos,
            "Variables:",
            fontsize=9,
            fontweight="bold",
            transform=ax.transAxes,
        )

        y_pos -= 0.025
        for var_name, var_value in list(self.variables.items())[
            :5
        ]:  # Limit to 5 variables
            display_value = str(var_value)
            if len(display_value) > 20:
                display_value = display_value[:17] + "..."
            ax.text(
                0.05,
                y_pos,
                f"  {var_name} = {display_value}",
                fontsize=8,
                fontfamily="monospace",
                transform=ax.transAxes,
            )
            y_pos -= 0.02

    def get_code_for_line(self, line_number: int) -> Optional[str]:
        """
        Get code for a specific line number.

        Args:
            line_number: Line number (0-indexed)

        Returns:
            Code line or None if out of range
        """
        if 0 <= line_number < len(self.lines):
            return self.lines[line_number]
        return None

    @classmethod
    def from_algorithm(cls, algorithm_name: str) -> "CodeOverlay":
        """
        Create code overlay from algorithm name using templates.

        Args:
            algorithm_name: Name of algorithm

        Returns:
            CodeOverlay instance
        """
        from ..templates.algorithm_templates import AlgorithmTemplates

        # Handle tree operations
        algorithm_lower = algorithm_name.lower()
        if "insert" in algorithm_lower and (
            "bst" in algorithm_lower or "tree" in algorithm_lower
        ):
            code = cls._get_bst_insert_code()
            return cls(code, "BST Insert")
        elif "search" in algorithm_lower and (
            "bst" in algorithm_lower or "tree" in algorithm_lower
        ):
            code = cls._get_bst_search_code()
            return cls(code, "BST Search")
        elif "delete" in algorithm_lower and (
            "bst" in algorithm_lower or "tree" in algorithm_lower
        ):
            code = cls._get_bst_delete_code()
            return cls(code, "BST Delete")
        elif "traversal" in algorithm_lower or "traverse" in algorithm_lower:
            code = cls._get_tree_traversal_code()
            return cls(code, "Tree Traversal")

        code = AlgorithmTemplates.get_template(algorithm_name)
        if not code or code == "# Template not available":
            # Fallback: try to get from algorithm class
            code = cls._get_code_from_algorithm(algorithm_name)

        return cls(code, algorithm_name)

    @classmethod
    def _get_bst_insert_code(cls) -> str:
        """Get BST insert code template."""
        return """def insert(root, value):
    # Base case: create new node
    if root is None:
        return TreeNode(value)

    # Recursive case: compare and go left or right
    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)

    return root"""

    @classmethod
    def _get_bst_search_code(cls) -> str:
        """Get BST search code template."""
        return """def search(root, value):
    # Base case: not found or found
    if root is None or root.value == value:
        return root

    # Recursive case: compare and search subtree
    if value < root.value:
        return search(root.left, value)
    else:
        return search(root.right, value)"""

    @classmethod
    def _get_bst_delete_code(cls) -> str:
        """Get BST delete code template."""
        return """def delete(root, value):
    # Base case: not found
    if root is None:
        return root

    # Find the node to delete
    if value < root.value:
        root.left = delete(root.left, value)
    elif value > root.value:
        root.right = delete(root.right, value)
    else:
        # Node found: handle deletion cases
        # Case 1: No children
        if root.left is None:
            return root.right
        # Case 2: One child
        elif root.right is None:
            return root.left
        # Case 3: Two children
        # Find inorder successor
        successor = find_min(root.right)
        root.value = successor.value
        root.right = delete(root.right, successor.value)

    return root"""

    @classmethod
    def _get_tree_traversal_code(cls) -> str:
        """Get tree traversal code template."""
        return """def inorder_traversal(root):
    # In-order: Left, Root, Right
    if root:
        inorder_traversal(root.left)
        visit(root.value)
        inorder_traversal(root.right)

def preorder_traversal(root):
    # Pre-order: Root, Left, Right
    if root:
        visit(root.value)
        preorder_traversal(root.left)
        preorder_traversal(root.right)

def postorder_traversal(root):
    # Post-order: Left, Right, Root
    if root:
        postorder_traversal(root.left)
        postorder_traversal(root.right)
        visit(root.value)"""

    @classmethod
    def _get_code_from_algorithm(cls, algorithm_name: str) -> str:
        """
        Try to get code from algorithm implementation.

        Args:
            algorithm_name: Name of algorithm

        Returns:
            Code string
        """
        # This is a fallback - in practice, templates should have the code
        return f"# Code for {algorithm_name}\n# Implementation not available"
