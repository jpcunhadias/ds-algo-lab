"""
Insights Panel
Displays algorithm complexity, properties, and educational insights.
"""

from typing import Dict, List, Optional


class AlgorithmInsights:
    """Stores algorithm insights and properties."""

    def __init__(
        self,
        name: str,
        time_complexity: str,
        space_complexity: str,
        properties: List[str],
        description: str = "",
    ):
        """
        Initialize algorithm insights.

        Args:
            name: Algorithm name
            time_complexity: Time complexity (e.g., "O(n²)")
            space_complexity: Space complexity (e.g., "O(1)")
            properties: List of properties (e.g., ["stable", "in-place"])
            description: Algorithm description
        """
        self.name = name
        self.time_complexity = time_complexity
        self.space_complexity = space_complexity
        self.properties = properties
        self.description = description


class InsightsPanel:
    """
    Displays algorithm insights including complexity and properties.
    """

    # Predefined insights for common algorithms
    ALGORITHM_INSIGHTS: Dict[str, AlgorithmInsights] = {
        "Bubble Sort": AlgorithmInsights(
            name="Bubble Sort",
            time_complexity="O(n²)",
            space_complexity="O(1)",
            properties=["stable", "in-place"],
            description="Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
        ),
        "Insertion Sort": AlgorithmInsights(
            name="Insertion Sort",
            time_complexity="O(n²)",
            space_complexity="O(1)",
            properties=["stable", "in-place", "adaptive"],
            description="Builds the final sorted array one item at a time by inserting each element into its correct position.",
        ),
        "Selection Sort": AlgorithmInsights(
            name="Selection Sort",
            time_complexity="O(n²)",
            space_complexity="O(1)",
            properties=["in-place"],
            description="Repeatedly finds the minimum element from unsorted part and puts it at the beginning.",
        ),
        "Merge Sort": AlgorithmInsights(
            name="Merge Sort",
            time_complexity="O(n log n)",
            space_complexity="O(n)",
            properties=["stable", "divide-and-conquer"],
            description="Divides the array into halves, sorts them, and merges them back together.",
        ),
        "Quick Sort": AlgorithmInsights(
            name="Quick Sort",
            time_complexity="O(n log n) average, O(n²) worst",
            space_complexity="O(log n)",
            properties=["in-place", "divide-and-conquer"],
            description="Picks a pivot element and partitions the array around the pivot.",
        ),
        "Heap Sort": AlgorithmInsights(
            name="Heap Sort",
            time_complexity="O(n log n)",
            space_complexity="O(1)",
            properties=["in-place"],
            description="Builds a max heap and repeatedly extracts the maximum element.",
        ),
        "Linear Search": AlgorithmInsights(
            name="Linear Search",
            time_complexity="O(n)",
            space_complexity="O(1)",
            properties=["simple"],
            description="Sequentially checks each element until the target is found or the list ends.",
        ),
        "Binary Search": AlgorithmInsights(
            name="Binary Search",
            time_complexity="O(log n)",
            space_complexity="O(1)",
            properties=["requires sorted array", "divide-and-conquer"],
            description="Searches a sorted array by repeatedly dividing the search interval in half.",
        ),
        "Ternary Search": AlgorithmInsights(
            name="Ternary Search",
            time_complexity="O(log₃ n)",
            space_complexity="O(1)",
            properties=["requires sorted array", "divide-and-conquer"],
            description="Divides the search space into three parts instead of two.",
        ),
        "Exponential Search": AlgorithmInsights(
            name="Exponential Search",
            time_complexity="O(log n)",
            space_complexity="O(1)",
            properties=["requires sorted array"],
            description="Finds the range where the target might be, then uses binary search.",
        ),
        # Tree operations
        "BST Insert": AlgorithmInsights(
            name="BST Insert",
            time_complexity="O(log n) average, O(n) worst",
            space_complexity="O(log n) recursive, O(1) iterative",
            properties=["maintains BST property", "recursive or iterative"],
            description="Inserts a value into a Binary Search Tree while maintaining the BST property (left < root < right).",
        ),
        "BST Search": AlgorithmInsights(
            name="BST Search",
            time_complexity="O(log n) average, O(n) worst",
            space_complexity="O(log n) recursive, O(1) iterative",
            properties=["divide-and-conquer", "uses BST property"],
            description="Searches for a value in a BST by comparing with root and recursively searching left or right subtree.",
        ),
        "BST Delete": AlgorithmInsights(
            name="BST Delete",
            time_complexity="O(log n) average, O(n) worst",
            space_complexity="O(log n) recursive, O(1) iterative",
            properties=["maintains BST property", "handles three cases"],
            description="Deletes a value from BST while maintaining the BST property. Handles cases: no children, one child, two children.",
        ),
        "Tree Traversal": AlgorithmInsights(
            name="Tree Traversal",
            time_complexity="O(n)",
            space_complexity="O(h) where h is height",
            properties=["visits all nodes", "multiple orderings"],
            description="Visits all nodes in a tree. Common orders: inorder (L-Root-R), preorder (Root-L-R), postorder (L-R-Root), level-order.",
        ),
    }

    def __init__(self, algorithm_name: str = ""):
        """
        Initialize insights panel.

        Args:
            algorithm_name: Name of the algorithm
        """
        self.algorithm_name = algorithm_name
        self.insights = self._get_insights(algorithm_name)

    def _get_insights(self, algorithm_name: str) -> Optional[AlgorithmInsights]:
        """
        Get insights for an algorithm.

        Args:
            algorithm_name: Name of the algorithm

        Returns:
            AlgorithmInsights or None
        """
        # Direct lookup
        if algorithm_name in self.ALGORITHM_INSIGHTS:
            return self.ALGORITHM_INSIGHTS[algorithm_name]

        # Try to match tree operations
        algorithm_lower = algorithm_name.lower()
        if "insert" in algorithm_lower and (
            "bst" in algorithm_lower or "tree" in algorithm_lower
        ):
            return self.ALGORITHM_INSIGHTS.get("BST Insert")
        elif "search" in algorithm_lower and (
            "bst" in algorithm_lower or "tree" in algorithm_lower
        ):
            return self.ALGORITHM_INSIGHTS.get("BST Search")
        elif "delete" in algorithm_lower and (
            "bst" in algorithm_lower or "tree" in algorithm_lower
        ):
            return self.ALGORITHM_INSIGHTS.get("BST Delete")
        elif "traversal" in algorithm_lower or "traverse" in algorithm_lower:
            return self.ALGORITHM_INSIGHTS.get("Tree Traversal")

        return None

    def render(self, ax, show_description: bool = True) -> None:
        """
        Render insights panel on matplotlib axes.

        Args:
            ax: Matplotlib axes to render on
            show_description: Whether to show algorithm description
        """
        ax.clear()
        ax.axis("off")

        if not self.insights:
            ax.text(
                0.5,
                0.5,
                "No insights available",
                ha="center",
                va="center",
                fontsize=10,
                color="gray",
                transform=ax.transAxes,
            )
            return

        y_pos = 0.95

        # Title
        ax.text(
            0.5,
            y_pos,
            "Algorithm Insights",
            fontsize=12,
            fontweight="bold",
            ha="center",
            transform=ax.transAxes,
        )

        y_pos -= 0.08

        # Algorithm name
        ax.text(
            0.1,
            y_pos,
            "Algorithm:",
            fontsize=10,
            fontweight="bold",
            transform=ax.transAxes,
        )
        ax.text(
            0.5,
            y_pos,
            self.insights.name,
            fontsize=10,
            color="#0066CC",
            transform=ax.transAxes,
        )

        y_pos -= 0.1

        # Time Complexity
        ax.text(
            0.1,
            y_pos,
            "Time Complexity:",
            fontsize=9,
            fontweight="bold",
            transform=ax.transAxes,
        )
        ax.text(
            0.5,
            y_pos,
            self.insights.time_complexity,
            fontsize=9,
            fontfamily="monospace",
            color="#CC6600",
            transform=ax.transAxes,
        )

        y_pos -= 0.08

        # Space Complexity
        ax.text(
            0.1,
            y_pos,
            "Space Complexity:",
            fontsize=9,
            fontweight="bold",
            transform=ax.transAxes,
        )
        ax.text(
            0.5,
            y_pos,
            self.insights.space_complexity,
            fontsize=9,
            fontfamily="monospace",
            color="#CC6600",
            transform=ax.transAxes,
        )

        y_pos -= 0.1

        # Properties
        if self.insights.properties:
            ax.text(
                0.1,
                y_pos,
                "Properties:",
                fontsize=9,
                fontweight="bold",
                transform=ax.transAxes,
            )

            y_pos -= 0.06
            props_text = ", ".join(self.insights.properties)
            ax.text(
                0.1,
                y_pos,
                props_text,
                fontsize=8,
                color="#006600",
                transform=ax.transAxes,
            )

            y_pos -= 0.1

        # Description
        if show_description and self.insights.description:
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
                "Description:",
                fontsize=9,
                fontweight="bold",
                transform=ax.transAxes,
            )

            y_pos -= 0.06

            # Wrap description text
            words = self.insights.description.split()
            lines = []
            current_line = ""
            for word in words:
                if len(current_line + word) < 40:
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                lines.append(current_line.strip())

            for line in lines[:4]:  # Limit to 4 lines
                ax.text(
                    0.1,
                    y_pos,
                    line,
                    fontsize=8,
                    transform=ax.transAxes,
                )
                y_pos -= 0.05

    @classmethod
    def get_insights(cls, algorithm_name: str) -> Optional[AlgorithmInsights]:
        """
        Get insights for an algorithm.

        Args:
            algorithm_name: Name of the algorithm

        Returns:
            AlgorithmInsights or None
        """
        return cls.ALGORITHM_INSIGHTS.get(algorithm_name)

    @classmethod
    def list_algorithms(cls) -> List[str]:
        """
        List all algorithms with available insights.

        Returns:
            List of algorithm names
        """
        return list(cls.ALGORITHM_INSIGHTS.keys())
