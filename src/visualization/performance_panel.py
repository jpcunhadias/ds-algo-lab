"""
Performance Panel
Displays real-time performance metrics during algorithm execution.
"""

from typing import Any, Dict, List, Optional

import matplotlib.patches as patches


class PerformanceMetrics:
    """Tracks performance metrics during algorithm execution."""

    def __init__(self):
        """Initialize performance metrics."""
        self.comparisons = 0
        self.swaps = 0
        self.operations = 0
        self.steps = 0
        self.start_time: Optional[float] = None
        self.history: List[Dict[str, int]] = []

    def reset(self) -> None:
        """Reset all metrics."""
        self.comparisons = 0
        self.swaps = 0
        self.operations = 0
        self.steps = 0
        self.start_time = None
        self.history = []

    def increment_comparison(self) -> None:
        """Increment comparison count."""
        self.comparisons += 1
        self.operations += 1
        self._record_step()

    def increment_swap(self) -> None:
        """Increment swap count."""
        self.swaps += 1
        self.operations += 1
        self._record_step()

    def increment_operation(self) -> None:
        """Increment general operation count."""
        self.operations += 1
        self._record_step()

    def increment_step(self) -> None:
        """Increment step count."""
        self.steps += 1
        self._record_step()

    def _record_step(self) -> None:
        """Record current metrics in history."""
        self.history.append(
            {
                "comparisons": self.comparisons,
                "swaps": self.swaps,
                "operations": self.operations,
                "steps": self.steps,
            }
        )

    def get_current_metrics(self) -> Dict[str, int]:
        """
        Get current metrics.

        Returns:
            Dictionary of current metrics
        """
        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "operations": self.operations,
            "steps": self.steps,
        }


class PerformancePanel:
    """
    Displays performance metrics during algorithm execution.
    """

    def __init__(self, metrics: Optional[PerformanceMetrics] = None):
        """
        Initialize performance panel.

        Args:
            metrics: PerformanceMetrics instance (optional)
        """
        self.metrics = metrics or PerformanceMetrics()
        self.theoretical_complexity: Optional[str] = None

    def set_theoretical_complexity(self, complexity: str) -> None:
        """
        Set theoretical complexity for comparison.

        Args:
            complexity: Complexity string (e.g., "O(n²)")
        """
        self.theoretical_complexity = complexity

    def extract_from_step(self, step: Dict[str, Any]) -> None:
        """
        Extract metrics from algorithm step.

        Args:
            step: Step dictionary
        """
        # Skip initialization steps - only count method operations
        if step.get("initialization", False):
            return

        # Sorting/searching algorithm metrics
        if "comparing" in step and step["comparing"]:
            self.metrics.increment_comparison()

        if "swapping" in step and step["swapping"]:
            self.metrics.increment_swap()

        # Tree operation metrics
        if "operation" in step:
            operation = step["operation"]
            # Skip initialization operations
            if operation in ["initialization_complete"]:
                return
            # Tree operations involve comparisons
            if operation in ["insert", "delete", "search"]:
                # Count comparisons based on path length
                if "highlighted_nodes" in step:
                    path = step["highlighted_nodes"]
                    if isinstance(path, list) and len(path) > 0:
                        # Each node in path represents a comparison
                        for _ in range(len(path)):
                            self.metrics.increment_comparison()
                # Also count if there's a current node being processed
                if "current_node" in step and step["current_node"] is not None:
                    self.metrics.increment_operation()

        # Graph operation metrics
        if "visited" in step:
            self.metrics.increment_operation()

        self.metrics.increment_step()

    def render(self, ax, show_history: bool = False) -> None:
        """
        Render performance panel on matplotlib axes.

        Args:
            ax: Matplotlib axes to render on
            show_history: Whether to show metric history graph
        """
        ax.clear()
        ax.axis("off")

        y_pos = 0.95

        # Title
        ax.text(
            0.5,
            y_pos,
            "Performance Metrics",
            fontsize=12,
            fontweight="bold",
            ha="center",
            transform=ax.transAxes,
        )

        y_pos -= 0.1

        metrics = self.metrics.get_current_metrics()

        # Comparisons
        ax.text(
            0.1,
            y_pos,
            "Comparisons:",
            fontsize=10,
            fontweight="bold",
            transform=ax.transAxes,
        )
        ax.text(
            0.6,
            y_pos,
            str(metrics["comparisons"]),
            fontsize=10,
            fontfamily="monospace",
            color="#0066CC",
            transform=ax.transAxes,
        )

        y_pos -= 0.08

        # Swaps
        ax.text(
            0.1,
            y_pos,
            "Swaps:",
            fontsize=10,
            fontweight="bold",
            transform=ax.transAxes,
        )
        ax.text(
            0.6,
            y_pos,
            str(metrics["swaps"]),
            fontsize=10,
            fontfamily="monospace",
            color="#CC6600",
            transform=ax.transAxes,
        )

        y_pos -= 0.08

        # Operations
        ax.text(
            0.1,
            y_pos,
            "Operations:",
            fontsize=10,
            fontweight="bold",
            transform=ax.transAxes,
        )
        ax.text(
            0.6,
            y_pos,
            str(metrics["operations"]),
            fontsize=10,
            fontfamily="monospace",
            color="#009900",
            transform=ax.transAxes,
        )

        y_pos -= 0.08

        # Steps
        ax.text(
            0.1,
            y_pos,
            "Steps:",
            fontsize=10,
            fontweight="bold",
            transform=ax.transAxes,
        )
        ax.text(
            0.6,
            y_pos,
            str(metrics["steps"]),
            fontsize=10,
            fontfamily="monospace",
            color="#666666",
            transform=ax.transAxes,
        )

        y_pos -= 0.12

        # Theoretical complexity
        if self.theoretical_complexity:
            # Draw separator
            ax.plot(
                [0.05, 0.95],
                [y_pos, y_pos],
                color="#CCCCCC",
                linewidth=1,
                transform=ax.transAxes,
            )

            y_pos -= 0.05

            ax.text(
                0.1,
                y_pos,
                "Theoretical:",
                fontsize=9,
                fontweight="bold",
                transform=ax.transAxes,
            )
            ax.text(
                0.5,
                y_pos,
                self.theoretical_complexity,
                fontsize=9,
                fontfamily="monospace",
                color="#CC6600",
                transform=ax.transAxes,
            )

            y_pos -= 0.1

        # Progress indicator
        if metrics["steps"] > 0:
            # Simple progress bar
            progress_width = 0.8
            progress_height = 0.03
            progress_x = 0.1
            progress_y = y_pos - 0.05

            # Background
            bg_rect = patches.Rectangle(
                (progress_x, progress_y),
                progress_width,
                progress_height,
                linewidth=1,
                edgecolor="#CCCCCC",
                facecolor="#F0F0F0",
                transform=ax.transAxes,
            )
            ax.add_patch(bg_rect)

            # Progress text
            ax.text(
                0.5,
                progress_y + progress_height / 2,
                f"Step {metrics['steps']}",
                fontsize=8,
                ha="center",
                va="center",
                transform=ax.transAxes,
            )

        # History graph
        if show_history and len(self.metrics.history) > 1:
            self._render_history_graph(ax, y_pos - 0.15)

    def _render_history_graph(self, ax, y_start: float) -> None:
        """
        Render metric history as a simple graph.

        Args:
            ax: Matplotlib axes
            y_start: Starting y position
        """
        if len(self.metrics.history) < 2:
            return

        # Draw separator
        ax.plot(
            [0.05, 0.95],
            [y_start, y_start],
            color="#CCCCCC",
            linewidth=1,
            transform=ax.transAxes,
        )

        y_start -= 0.05

        # Simple line graph for operations
        history = self.metrics.history[-20:]  # Last 20 steps
        if len(history) < 2:
            return

        x_coords = [0.1 + (i / (len(history) - 1)) * 0.8 for i in range(len(history))]
        y_coords = [
            y_start
            + (
                h["operations"]
                / max(h["operations"] for h in history if h["operations"] > 0)
            )
            * 0.1
            if max(h["operations"] for h in history if h["operations"] > 0) > 0
            else y_start
            for h in history
        ]

        ax.plot(
            x_coords,
            y_coords,
            color="#0066CC",
            linewidth=2,
            transform=ax.transAxes,
        )

        ax.text(
            0.1,
            y_start - 0.02,
            "Operations over time",
            fontsize=7,
            color="gray",
            transform=ax.transAxes,
        )
