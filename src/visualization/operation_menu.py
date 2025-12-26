"""
Operation Menu
GUI menu for selecting data structure operations after initialization.
"""

from typing import Any, Callable, Dict, List, Optional

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox


class OperationMenu:
    """
    GUI menu dialog for selecting and executing data structure operations.
    """

    def __init__(
        self,
        available_operations: List[str],
        operation_handler: Callable[[str, Dict[str, Any]], None],
        title: str = "Select Operation",
    ):
        """
        Initialize operation menu.

        Args:
            available_operations: List of operation names (e.g., ['insert', 'delete', 'search'])
            operation_handler: Callback function that handles operation execution
                              Signature: handler(operation_name: str, params: Dict[str, Any]) -> None
            title: Menu title
        """
        self.available_operations = available_operations
        self.operation_handler = operation_handler
        self.title = title
        self.fig = None
        self.selected_operation = None
        self.operation_params = {}
        self.text_box = None

    def show(self) -> Optional[str]:
        """
        Show the operation menu dialog.

        Returns:
            Selected operation name or None if cancelled
        """
        self.fig = plt.figure(figsize=(10, 6))
        self.fig.suptitle(self.title, fontsize=14, fontweight="bold")

        # Calculate button layout
        num_ops = len(self.available_operations)
        cols = min(3, num_ops)
        rows = (num_ops + cols - 1) // cols

        buttons = []
        button_width = 0.25
        button_height = 0.08
        spacing_x = 0.05
        spacing_y = 0.12
        start_x = 0.1
        start_y = 0.7

        for i, operation in enumerate(self.available_operations):
            row = i // cols
            col = i % cols

            x_pos = start_x + col * (button_width + spacing_x)
            y_pos = start_y - row * (button_height + spacing_y)

            ax_btn = plt.axes([x_pos, y_pos, button_width, button_height])
            btn = Button(ax_btn, operation.title())
            btn.on_clicked(lambda event, op=operation: self._on_operation_click(op))
            buttons.append(btn)

        # Add input field for operations that need a value
        ax_input = plt.axes([0.1, 0.35, 0.3, 0.05])
        self.text_box = TextBox(ax_input, "Value: ", initial="", textalignment="left")

        # Add traversal type selector (for traverse operation)
        if "traverse" in self.available_operations:
            ax_traversal_label = plt.axes([0.1, 0.25, 0.15, 0.05])
            ax_traversal_label.axis("off")
            ax_traversal_label.text(
                0,
                0.5,
                "Traversal:",
                fontsize=10,
                va="center",
                transform=ax_traversal_label.transAxes,
            )

            self.traversal_buttons = {}
            traversal_types = ["inorder", "preorder", "postorder", "levelorder"]
            traversal_start_x = 0.25
            for i, trav_type in enumerate(traversal_types):
                ax_trav = plt.axes([traversal_start_x + i * 0.15, 0.25, 0.12, 0.05])
                btn_trav = Button(ax_trav, trav_type[:4])  # Shortened label
                btn_trav.on_clicked(
                    lambda event, t=trav_type: self._set_traversal_type(t)
                )
                self.traversal_buttons[trav_type] = btn_trav
            self.selected_traversal = "inorder"
        else:
            self.selected_traversal = "inorder"

        # Add close button
        ax_close = plt.axes([0.6, 0.1, 0.2, 0.05])
        btn_close = Button(ax_close, "Close")
        btn_close.on_clicked(self._on_close)

        # Store references
        self._buttons = buttons
        self._btn_close = btn_close

        plt.show(block=True)
        return self.selected_operation

    def _on_operation_click(self, operation: str):
        """Handle operation button click."""
        self.selected_operation = operation

        # Get value from text box if needed
        value = None
        if self.text_box:
            try:
                value_text = self.text_box.text
                if value_text.strip():
                    # Try to convert to int, fallback to string
                    try:
                        value = int(value_text)
                    except ValueError:
                        value = value_text
            except:
                pass

        # Prepare parameters
        params = {}
        if value is not None:
            params["value"] = value

        # Handle operation-specific parameters
        if operation == "traverse":
            params["traversal_type"] = getattr(self, "selected_traversal", "inorder")

        # Call handler
        if self.operation_handler:
            self.operation_handler(operation, params)

        # Close menu
        plt.close(self.fig)

    def _set_traversal_type(self, traversal_type: str):
        """Set selected traversal type."""
        self.selected_traversal = traversal_type

    def _on_close(self, event):
        """Handle close button click."""
        plt.close(self.fig)
