"""
Algorithm Visualizer
Provides animated visualizations for algorithms with step-by-step execution.
"""

from typing import Any, Dict, List, Optional

from .base import BaseDataStructure, BaseVisualizer


class AlgorithmVisualizer(BaseVisualizer):
    """
    Visualizer for algorithms with animated step-by-step execution.
    """

    def __init__(self, animation_speed: float = 0.5):
        """
        Initialize the algorithm visualizer.

        Args:
            animation_speed: Speed of animation in seconds per frame
        """
        super().__init__()
        self._animation_speed = animation_speed
        self._steps = []
        self._current_step_index = 0

    def visualize(
        self,
        data_structure: BaseDataStructure,
        step: Optional[Dict[str, Any]] = None,
        ax=None,
        fig=None,
    ):
        """
        Visualize the current state during algorithm execution.

        Args:
            data_structure: The data structure being operated on
            step: Step information containing algorithm state
            ax: Optional matplotlib axes to draw on (if None, creates new figure)
            fig: Optional matplotlib figure (used with ax)
        """
        import matplotlib.pyplot as plt

        if step is None:
            return

        # Use provided axes or create new figure
        if ax is not None:
            self._axes = ax
            self._figure = fig
            # Clear axes when reusing (important for animation updates)
            self._axes.clear()
        else:
            # Create figure only if not provided
            self._figure, self._axes = plt.subplots(figsize=(12, 6))

        self._axes.set_xlim(-1, max(len(data_structure), 10))
        self._axes.set_ylim(-0.5, 2.5)
        self._axes.set_aspect("equal")
        self._axes.axis("off")

        # Get algorithm-specific visualization
        algo_type = step.get("algorithm", "unknown")

        if "sort" in algo_type.lower():
            self._visualize_sorting_step(data_structure, step)
        elif "search" in algo_type.lower():
            self._visualize_searching_step(data_structure, step)

        # Add title with step info (only if we created the figure ourselves)
        if ax is None:
            title = f"{algo_type} - Step {step.get('step_number', 'N/A')}"
            if "description" in step:
                title += f": {step['description']}"
            self._axes.set_title(title, fontsize=14, fontweight="bold")
            plt.tight_layout()

    def _visualize_sorting_step(
        self, data_structure: BaseDataStructure, step: Dict[str, Any]
    ):
        """Visualize a sorting algorithm step."""
        import matplotlib.patches as patches

        # Get data from state to avoid type checking issues
        state = data_structure.get_state()
        data = state.get("data", [])

        # Get algorithm name to determine visualization style
        algo_name = step.get("algorithm", "").lower()

        # Get step-specific information
        comparing = step.get("comparing", [])
        swapping = step.get("swapping", [])
        sorted_indices = step.get("sorted", [])
        current_indices = step.get("current", [])

        # Merge Sort specific visualization
        if "merge" in algo_name:
            left_range = step.get("left_range")
            right_range = step.get("right_range")

            for i, value in enumerate(data):
                # Determine color based on state
                if i in swapping:
                    color = "red"  # Elements being swapped
                elif i in comparing:
                    color = "yellow"  # Elements being compared
                elif i in sorted_indices:
                    color = "green"  # Already sorted
                elif left_range and right_range:
                    left_start, left_end = left_range
                    right_start, right_end = right_range
                    if left_start <= i <= left_end:
                        color = "lightcoral"  # Left subarray
                    elif right_start <= i <= right_end:
                        color = "lightblue"  # Right subarray
                    else:
                        color = "lightgray"  # Outside merge range
                elif i in current_indices:
                    color = "orange"  # Current position
                else:
                    color = "lightblue"  # Default

                # Draw rectangle
                rect = patches.Rectangle(
                    (i - 0.4, 0.5),
                    0.8,
                    1,
                    linewidth=2,
                    edgecolor="black",
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

                # Add index
                self._axes.text(
                    i, 0.2, str(i), ha="center", va="center", fontsize=10, color="gray"
                )

            # Add merge range indicators
            if left_range and right_range:
                left_start, left_end = left_range
                right_start, right_end = right_range
                # Draw brackets for merge ranges
                self._axes.plot(
                    [left_start - 0.5, left_start - 0.5], [0.3, 1.7], "k-", linewidth=2
                )
                self._axes.plot(
                    [left_end + 0.5, left_end + 0.5], [0.3, 1.7], "k-", linewidth=2
                )
                self._axes.plot(
                    [right_start - 0.5, right_start - 0.5],
                    [0.3, 1.7],
                    "k-",
                    linewidth=2,
                )
                self._axes.plot(
                    [right_end + 0.5, right_end + 0.5], [0.3, 1.7], "k-", linewidth=2
                )

        # Quick Sort specific visualization
        elif "quick" in algo_name:
            pivot = step.get("pivot")
            partition = step.get("partition")

            for i, value in enumerate(data):
                # Determine color based on state
                if i == pivot:
                    color = "purple"  # Pivot element
                elif i in swapping:
                    color = "red"  # Elements being swapped
                elif i in comparing:
                    color = "yellow"  # Elements being compared
                elif i in sorted_indices:
                    color = "green"  # Already sorted (pivot in final position)
                elif partition:
                    part_low = partition.get("low", -1)
                    part_high = partition.get("high", -1)
                    if part_low <= i <= part_high:
                        color = "lightblue"  # Partition range
                    else:
                        color = "lightgray"  # Outside partition
                elif i in current_indices:
                    color = "orange"  # Current position
                else:
                    color = "lightblue"  # Default

                # Draw rectangle
                rect = patches.Rectangle(
                    (i - 0.4, 0.5),
                    0.8,
                    1,
                    linewidth=2,
                    edgecolor="black",
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

                # Add index
                self._axes.text(
                    i, 0.2, str(i), ha="center", va="center", fontsize=10, color="gray"
                )

            # Add pivot indicator
            if pivot is not None:
                self._axes.text(
                    pivot,
                    1.8,
                    "PIVOT",
                    ha="center",
                    va="center",
                    fontsize=10,
                    fontweight="bold",
                    color="purple",
                )

        # Heap Sort specific visualization
        elif "heap" in algo_name:
            heap_info = step.get("heap")

            for i, value in enumerate(data):
                # Determine color based on state
                if i in swapping:
                    color = "red"  # Elements being swapped
                elif i in comparing:
                    color = "yellow"  # Elements being compared
                elif i in sorted_indices:
                    color = "green"  # Already sorted (extracted from heap)
                elif heap_info:
                    heap_indices = heap_info.get("heap_indices", [])
                    root = heap_info.get("root")
                    left = heap_info.get("left")
                    right = heap_info.get("right")
                    if i == root:
                        color = "purple"  # Root being heapified
                    elif i == left or i == right:
                        color = "orange"  # Children being compared
                    elif i in heap_indices:
                        color = "lightblue"  # In heap
                    else:
                        color = "lightgray"  # Outside heap
                elif i in current_indices:
                    color = "orange"  # Current position
                else:
                    color = "lightblue"  # Default

                # Draw rectangle
                rect = patches.Rectangle(
                    (i - 0.4, 0.5),
                    0.8,
                    1,
                    linewidth=2,
                    edgecolor="black",
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

                # Add index
                self._axes.text(
                    i, 0.2, str(i), ha="center", va="center", fontsize=10, color="gray"
                )

                # Draw parent-child relationships for heap
                if heap_info and i in heap_info.get("heap_indices", []):
                    parent_idx = (i - 1) // 2
                    if parent_idx >= 0 and parent_idx < len(data):
                        # Draw line from parent to child
                        self._axes.plot(
                            [parent_idx, i], [1.3, 1.3], "k-", linewidth=1, alpha=0.3
                        )

        # Default visualization for other sorting algorithms
        else:
            for i, value in enumerate(data):
                # Determine color based on state
                if i in swapping:
                    color = "red"  # Elements being swapped
                elif i in comparing:
                    color = "yellow"  # Elements being compared
                elif i in sorted_indices:
                    color = "green"  # Already sorted
                elif i in current_indices:
                    color = "orange"  # Current position
                else:
                    color = "lightblue"  # Default

                # Draw rectangle
                rect = patches.Rectangle(
                    (i - 0.4, 0.5),
                    0.8,
                    1,
                    linewidth=2,
                    edgecolor="black",
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

                # Add index
                self._axes.text(
                    i, 0.2, str(i), ha="center", va="center", fontsize=10, color="gray"
                )

        # Add legend
        legend_elements = [
            patches.Patch(facecolor="lightblue", label="Normal"),
            patches.Patch(facecolor="yellow", label="Comparing"),
            patches.Patch(facecolor="red", label="Swapping"),
            patches.Patch(facecolor="green", label="Sorted"),
        ]
        self._axes.legend(handles=legend_elements, loc="upper right")

    def _visualize_searching_step(
        self, data_structure: BaseDataStructure, step: Dict[str, Any]
    ):
        """Visualize a searching algorithm step."""
        import matplotlib.patches as patches

        # Get data from state to avoid type checking issues
        state = data_structure.get_state()
        data = state.get("data", [])
        target = step.get("target", None)
        current_index = step.get("current_index", -1)
        found_index = step.get("found_index", -1)
        algo_name = step.get("algorithm", "").lower()

        # Ternary Search specific visualization
        if "ternary" in algo_name:
            left = step.get("left", 0)
            right = step.get("right", len(data) - 1)
            mid1 = step.get("mid1", -1)
            mid2 = step.get("mid2", -1)

            for i, value in enumerate(data):
                # Determine color
                if i == found_index:
                    color = "green"  # Found
                elif i == mid1 or i == mid2:
                    color = "yellow"  # Currently checking (mid1 or mid2)
                elif i == current_index:
                    color = "orange"  # Current position
                elif left <= i <= right:
                    color = "lightblue"  # Search range
                else:
                    color = "lightgray"  # Outside search range

                # Draw rectangle
                rect = patches.Rectangle(
                    (i - 0.4, 0.5),
                    0.8,
                    1,
                    linewidth=2,
                    edgecolor="black",
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

                # Add index
                self._axes.text(
                    i, 0.2, str(i), ha="center", va="center", fontsize=10, color="gray"
                )

                # Mark mid1 and mid2
                if i == mid1:
                    self._axes.text(
                        i,
                        1.8,
                        "mid1",
                        ha="center",
                        va="center",
                        fontsize=9,
                        fontweight="bold",
                        color="darkorange",
                    )
                if i == mid2:
                    self._axes.text(
                        i,
                        1.8,
                        "mid2",
                        ha="center",
                        va="center",
                        fontsize=9,
                        fontweight="bold",
                        color="darkorange",
                    )

        # Exponential Search specific visualization
        elif "exponential" in algo_name:
            left = step.get("left", 0)
            right = step.get("right", len(data) - 1)
            range_start = step.get("range_start", -1)
            range_end = step.get("range_end", -1)
            phase = step.get("phase", "")

            for i, value in enumerate(data):
                # Determine color
                if i == found_index:
                    color = "green"  # Found
                elif i == current_index:
                    color = "yellow"  # Currently checking
                elif (
                    range_start != -1
                    and range_end != -1
                    and range_start <= i <= range_end
                ):
                    if phase == "exponential_range_finding":
                        color = "lightcoral"  # Exponential range
                    else:
                        color = "lightblue"  # Binary search range
                elif target is not None and value == target:
                    color = "orange"  # Potential match
                else:
                    color = "lightgray"  # Outside range

                # Draw rectangle
                rect = patches.Rectangle(
                    (i - 0.4, 0.5),
                    0.8,
                    1,
                    linewidth=2,
                    edgecolor="black",
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

                # Add index
                self._axes.text(
                    i, 0.2, str(i), ha="center", va="center", fontsize=10, color="gray"
                )

            # Show phase info
            if phase:
                phase_text = phase.replace("_", " ").title()
                self._axes.text(
                    len(data) / 2,
                    1.8,
                    f"Phase: {phase_text}",
                    ha="center",
                    va="center",
                    fontsize=10,
                    fontweight="bold",
                    color="purple",
                )

        # Default visualization for other searching algorithms
        else:
            left = step.get("left", 0)
            right = step.get("right", len(data) - 1)

            for i, value in enumerate(data):
                # Determine color
                if i == found_index:
                    color = "green"  # Found
                elif i == current_index:
                    color = "yellow"  # Currently checking
                elif left <= i <= right:
                    color = "lightblue"  # Search range
                elif target is not None and value == target:
                    color = "orange"  # Potential match
                else:
                    color = "lightgray"  # Outside search range

                # Draw rectangle
                rect = patches.Rectangle(
                    (i - 0.4, 0.5),
                    0.8,
                    1,
                    linewidth=2,
                    edgecolor="black",
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

                # Add index
                self._axes.text(
                    i, 0.2, str(i), ha="center", va="center", fontsize=10, color="gray"
                )

        # Add target value info
        if target is not None:
            self._axes.text(
                0,
                2,
                f"Searching for: {target}",
                ha="left",
                va="center",
                fontsize=12,
                fontweight="bold",
            )

        if found_index != -1:
            self._axes.text(
                0,
                1.7,
                f"Found at index: {found_index}",
                ha="left",
                va="center",
                fontsize=11,
                color="green",
                fontweight="bold",
            )

    def animate(self, steps: List[Dict[str, Any]]):
        """
        Animate through a series of algorithm steps.

        Args:
            steps: List of step dictionaries to animate
        """
        import matplotlib.animation as animation
        import matplotlib.pyplot as plt

        self._steps = steps

        if not steps:
            return

        # Create animation
        fig, ax = plt.subplots(figsize=(12, 6))

        def animate_frame(frame):  # type: ignore[misc]
            ax.clear()
            step = steps[frame]
            data_structure = step.get("data_structure")

            if data_structure:
                ax.set_xlim(-1, max(len(data_structure), 10))
                ax.set_ylim(-0.5, 2.5)
                ax.set_aspect("equal")
                ax.axis("off")

                if "sort" in step.get("algorithm", "").lower():
                    self._visualize_sorting_step(data_structure, step)
                elif "search" in step.get("algorithm", "").lower():
                    self._visualize_searching_step(data_structure, step)
            else:
                ax.set_xlim(-1, 10)
                ax.set_ylim(-0.5, 2.5)
                ax.set_aspect("equal")
                ax.axis("off")

            title = (
                f"{step.get('algorithm', 'Algorithm')} - Step {frame + 1}/{len(steps)}"
            )
            if "description" in step:
                title += f": {step['description']}"
            ax.set_title(title, fontsize=14, fontweight="bold")

        # FuncAnimation accepts functions that return None, despite type stubs
        _ = animation.FuncAnimation(  # pyright: ignore[reportArgumentType]
            fig,
            animate_frame,
            frames=len(steps),
            interval=self._animation_speed * 1000,
            repeat=False,
        )

        plt.tight_layout()
        plt.show()

    def step_by_step(self, steps: List[Dict[str, Any]]):
        """
        Display steps one at a time with user control.

        Args:
            steps: List of step dictionaries
        """
        import matplotlib.pyplot as plt

        self._steps = steps
        self._current_step_index = 0

        print("Step-by-step mode:")
        print("Press Enter to advance to next step, 'q' to quit")

        for i, step in enumerate(steps):
            data_structure = step.get("data_structure")
            if data_structure:
                self.visualize(data_structure, step)
                plt.show(block=False)

                user_input = input(
                    f"Step {i + 1}/{len(steps)} - Press Enter to continue (q to quit): "
                )
                if user_input.lower() == "q":
                    break
                plt.close()

        plt.close("all")
