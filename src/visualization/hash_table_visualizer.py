"""
Hash Table Visualizer
Provides visualizations for hash tables showing buckets, collisions, and operations.
"""

from typing import Any, Dict, List, Optional
from .base import BaseDataStructure, BaseVisualizer


class HashTableVisualizer(BaseVisualizer):
    """
    Visualizer for hash table data structures.
    Shows buckets, collisions, and hash function calculations.
    """

    def __init__(self):
        """Initialize the hash table visualizer."""
        super().__init__()
        self._bucket_width = 1.2
        self._bucket_height = 1.5
        self._entry_height = 0.3

    def visualize(
        self,
        data_structure: BaseDataStructure,
        step: Optional[Dict[str, Any]] = None,
        ax=None,
        fig=None,
    ):
        """
        Visualize a hash table.

        Args:
            data_structure: The hash table to visualize
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
            self._figure, self._axes = plt.subplots(figsize=(14, 8))

        state = data_structure.get_state()
        hash_table_data = state.get("data", {})

        if not hash_table_data:
            self._axes.text(
                0,
                0,
                "Empty Hash Table",
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold",
            )
            self._axes.axis("off")
            return

        capacity = hash_table_data.get("capacity", 16)
        size = hash_table_data.get("size", 0)
        load_factor = hash_table_data.get("load_factor", 0.0)
        buckets = hash_table_data.get("buckets", [])

        # Get operation info from step
        operation = step.get("operation", "normal") if step else "normal"
        current_key = step.get("key", None) if step else None
        current_bucket = step.get("bucket_index", None) if step else None
        hash_value = step.get("hash_value", None) if step else None

        # Draw buckets
        self._draw_buckets(buckets, capacity, current_bucket, current_key)

        # Draw hash calculation if present
        if hash_value is not None and current_key is not None:
            self._draw_hash_calculation(current_key, hash_value, current_bucket)

        # Draw load factor and stats
        self._draw_stats(size, capacity, load_factor)

        # Set axis limits
        self._axes.set_xlim(-1, capacity + 1)
        self._axes.set_ylim(-2, 4)
        self._axes.set_aspect("equal")
        self._axes.axis("off")

        # Add title
        ds_type = state.get("type", "HashTable")
        title = f"{ds_type} Visualization"
        if step:
            if "operation" in step:
                title += f" - {step['operation'].title()}"
            if "step_number" in step:
                title += f" (Step {step['step_number']})"
        self._axes.set_title(title, fontsize=14, fontweight="bold", pad=20)

    def _draw_buckets(
        self,
        buckets: List[Dict[str, Any]],
        capacity: int,
        current_bucket: Optional[int],
        current_key: Optional[Any],
    ) -> None:
        """
        Draw hash table buckets.

        Args:
            buckets: List of bucket data
            capacity: Total capacity
            current_bucket: Currently active bucket
            current_key: Currently active key
        """
        import matplotlib.patches as patches

        for i in range(capacity):
            bucket_data = None
            for b in buckets:
                if b.get("index") == i:
                    bucket_data = b
                    break

            x = i
            y_bottom = 0

            # Determine bucket color
            bucket_color = "lightgray"
            edge_color = "black"
            edge_width = 1.5

            if i == current_bucket:
                bucket_color = "yellow"
                edge_color = "red"
                edge_width = 3

            # Draw bucket rectangle
            rect = patches.Rectangle(
                (x - self._bucket_width / 2, y_bottom),
                self._bucket_width,
                self._bucket_height,
                linewidth=edge_width,
                edgecolor=edge_color,
                facecolor=bucket_color,
            )
            self._axes.add_patch(rect)

            # Draw bucket index
            self._axes.text(
                x,
                y_bottom - 0.3,
                f"Bucket {i}",
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
            )

            # Draw entries in bucket (chaining)
            if bucket_data:
                entries = bucket_data.get("entries", [])
                y_offset = y_bottom + self._bucket_height - 0.1

                for j, (key, value) in enumerate(entries):
                    entry_y = y_offset - j * (self._entry_height + 0.05)

                    # Determine entry color
                    entry_color = "lightblue"
                    entry_edge = "blue"
                    if key == current_key:
                        entry_color = "orange"
                        entry_edge = "red"

                    # Draw entry rectangle
                    entry_rect = patches.Rectangle(
                        (x - self._bucket_width / 2 + 0.05, entry_y - self._entry_height / 2),
                        self._bucket_width - 0.1,
                        self._entry_height,
                        linewidth=1.5,
                        edgecolor=entry_edge,
                        facecolor=entry_color,
                    )
                    self._axes.add_patch(entry_rect)

                    # Draw key-value text
                    self._axes.text(
                        x,
                        entry_y,
                        f"{key}:{value}",
                        ha="center",
                        va="center",
                        fontsize=8,
                        fontweight="bold",
                    )

                    # Draw chain arrow if not last entry
                    if j < len(entries) - 1:
                        arrow_y = entry_y - self._entry_height / 2 - 0.05
                        self._axes.annotate(
                            "",
                            xy=(x, arrow_y - 0.1),
                            xytext=(x, arrow_y),
                            arrowprops=dict(arrowstyle="->", lw=1, color="gray"),
                        )

    def _draw_hash_calculation(self, key: Any, hash_value: int, bucket_index: int) -> None:
        """
        Draw hash function calculation.

        Args:
            key: Key being hashed
            hash_value: Hash value
            bucket_index: Resulting bucket index
        """
        # Draw calculation above buckets
        calc_y = 3.5
        calc_x = bucket_index if bucket_index is not None else 0

        # Show hash calculation
        calc_text = f"hash({key}) = {hash_value}"
        if bucket_index is not None:
            calc_text += f" % capacity = {bucket_index}"

        self._axes.text(
            calc_x,
            calc_y,
            calc_text,
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="yellow", alpha=0.8),
        )

    def _draw_stats(self, size: int, capacity: int, load_factor: float) -> None:
        """
        Draw hash table statistics.

        Args:
            size: Current size
            capacity: Capacity
            load_factor: Load factor
        """
        stats_x = capacity / 2
        stats_y = -1.5

        stats_text = f"Size: {size} | Capacity: {capacity} | Load Factor: {load_factor:.2f}"

        self._axes.text(
            stats_x,
            stats_y,
            stats_text,
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.7),
        )

    def visualize_insert(
        self, data_structure: BaseDataStructure, key: Any, value: Any, bucket_index: int, hash_value: int
    ):
        """
        Visualize insert operation.

        Args:
            data_structure: The hash table
            key: Key being inserted
            value: Value being inserted
            bucket_index: Bucket index
            hash_value: Hash value
        """
        step = {
            "operation": "insert",
            "key": key,
            "value": value,
            "bucket_index": bucket_index,
            "hash_value": hash_value,
            "description": f"Inserting {key}:{value}",
        }
        self.visualize(data_structure, step)

    def visualize_get(
        self, data_structure: BaseDataStructure, key: Any, bucket_index: int, hash_value: int, found: bool
    ):
        """
        Visualize get operation.

        Args:
            data_structure: The hash table
            key: Key being searched
            bucket_index: Bucket index
            hash_value: Hash value
            found: Whether key was found
        """
        step = {
            "operation": "get",
            "key": key,
            "bucket_index": bucket_index,
            "hash_value": hash_value,
            "found": found,
            "description": f"Getting {key}",
        }
        self.visualize(data_structure, step)

    def visualize_delete(
        self, data_structure: BaseDataStructure, key: Any, bucket_index: int, hash_value: int
    ):
        """
        Visualize delete operation.

        Args:
            data_structure: The hash table
            key: Key being deleted
            bucket_index: Bucket index
            hash_value: Hash value
        """
        step = {
            "operation": "delete",
            "key": key,
            "bucket_index": bucket_index,
            "hash_value": hash_value,
            "description": f"Deleting {key}",
        }
        self.visualize(data_structure, step)

    def visualize_resize(
        self, data_structure: BaseDataStructure, old_capacity: int, new_capacity: int
    ):
        """
        Visualize resize operation.

        Args:
            data_structure: The hash table
            old_capacity: Old capacity
            new_capacity: New capacity
        """
        step = {
            "operation": "resize",
            "old_capacity": old_capacity,
            "new_capacity": new_capacity,
            "description": f"Resizing from {old_capacity} to {new_capacity}",
        }
        self.visualize(data_structure, step)

    def animate(self, steps: List[Dict[str, Any]]):
        """
        Animate through a series of hash table operation steps.

        Args:
            steps: List of step dictionaries
        """
        import matplotlib.animation as animation
        import matplotlib.pyplot as plt

        if not steps:
            return

        fig, ax = plt.subplots(figsize=(14, 8))

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

