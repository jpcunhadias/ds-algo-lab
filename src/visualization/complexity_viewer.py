"""
Complexity Viewer
Visualizes actual vs theoretical algorithm complexity.
"""

from typing import Dict, Any, Optional, List, Tuple
import matplotlib.pyplot as plt
import numpy as np


class ComplexityViewer:
    """
    Visualizes algorithm complexity comparison.
    """

    def __init__(self):
        """Initialize complexity viewer."""
        self.input_sizes: List[int] = []
        self.actual_operations: List[int] = []
        self.theoretical_operations: List[float] = []
        self.algorithm_name: str = ""

    def add_data_point(
        self, input_size: int, actual_ops: int, theoretical_ops: Optional[float] = None
    ) -> None:
        """
        Add a data point.

        Args:
            input_size: Input size (n)
            actual_ops: Actual number of operations
            theoretical_ops: Theoretical number of operations (optional)
        """
        self.input_sizes.append(input_size)
        self.actual_operations.append(actual_ops)
        if theoretical_ops is not None:
            self.theoretical_operations.append(theoretical_ops)
        else:
            self.theoretical_operations.append(0)

    def set_algorithm(self, algorithm_name: str) -> None:
        """
        Set algorithm name.

        Args:
            algorithm_name: Name of algorithm
        """
        self.algorithm_name = algorithm_name

    def calculate_theoretical(self, complexity: str, input_size: int) -> float:
        """
        Calculate theoretical operations for given complexity.

        Args:
            complexity: Complexity string (e.g., "O(n²)", "O(n log n)")
            input_size: Input size

        Returns:
            Theoretical operation count
        """
        complexity_lower = complexity.lower().replace(" ", "")

        if "n²" in complexity_lower or "n^2" in complexity_lower:
            return input_size * input_size
        elif "nlogn" in complexity_lower or "n*log(n)" in complexity_lower:
            return input_size * np.log2(max(input_size, 1))
        elif "logn" in complexity_lower or "log(n)" in complexity_lower:
            return np.log2(max(input_size, 1))
        elif "n" in complexity_lower and "log" not in complexity_lower:
            return input_size
        else:
            return 1  # O(1)

    def render(self, ax) -> None:
        """
        Render complexity comparison graph.

        Args:
            ax: Matplotlib axes to render on
        """
        if not self.input_sizes:
            ax.text(
                0.5,
                0.5,
                "No data available",
                ha="center",
                va="center",
                fontsize=10,
                color="gray",
                transform=ax.transAxes,
            )
            return

        # Plot actual operations
        ax.plot(
            self.input_sizes,
            self.actual_operations,
            "o-",
            label="Actual",
            color="#0066CC",
            linewidth=2,
            markersize=6,
        )

        # Plot theoretical operations if available
        if self.theoretical_operations and any(op > 0 for op in self.theoretical_operations):
            ax.plot(
                self.input_sizes,
                self.theoretical_operations,
                "--",
                label="Theoretical",
                color="#CC6600",
                linewidth=2,
            )

        ax.set_xlabel("Input Size (n)", fontsize=10, fontweight="bold")
        ax.set_ylabel("Operations", fontsize=10, fontweight="bold")
        ax.set_title(
            f"Complexity Analysis: {self.algorithm_name}" if self.algorithm_name else "Complexity Analysis",
            fontsize=11,
            fontweight="bold",
        )
        ax.legend(loc="upper left", fontsize=9)
        ax.grid(True, alpha=0.3)

    def render_comparison(
        self, fig, algorithms_data: Dict[str, Tuple[List[int], List[int]]]
    ) -> None:
        """
        Render comparison of multiple algorithms.

        Args:
            fig: Matplotlib figure
            algorithms_data: Dictionary mapping algorithm names to (input_sizes, operations) tuples
        """
        num_algorithms = len(algorithms_data)
        if num_algorithms == 0:
            return

        # Create subplots
        cols = min(2, num_algorithms)
        rows = (num_algorithms + cols - 1) // cols

        for i, (algo_name, (input_sizes, operations)) in enumerate(algorithms_data.items()):
            ax = fig.add_subplot(rows, cols, i + 1)

            ax.plot(
                input_sizes,
                operations,
                "o-",
                label=algo_name,
                linewidth=2,
                markersize=5,
            )

            ax.set_xlabel("Input Size", fontsize=9)
            ax.set_ylabel("Operations", fontsize=9)
            ax.set_title(algo_name, fontsize=10, fontweight="bold")
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=8)

        plt.tight_layout()

    def clear(self) -> None:
        """Clear all data."""
        self.input_sizes = []
        self.actual_operations = []
        self.theoretical_operations = []
        self.algorithm_name = ""

