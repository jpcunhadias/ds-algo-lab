"""
Graph Visualizer
Provides graph visualizations with force-directed layout and algorithm state visualization.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from .base import BaseDataStructure, BaseVisualizer


class GraphVisualizer(BaseVisualizer):
    """
    Visualizer for graph data structures.
    Provides force-directed layout and BFS/DFS visualization.
    """

    def __init__(self):
        """Initialize the graph visualizer."""
        super().__init__()
        self._node_positions: Dict[Any, Tuple[float, float]] = {}
        self._node_radius = 0.4
        self._layout_type = "force_directed"  # or "circular", "hierarchical"

    def visualize(
        self,
        data_structure: BaseDataStructure,
        step: Optional[Dict[str, Any]] = None,
        ax=None,
        fig=None,
    ):
        """
        Visualize a graph data structure.

        Args:
            data_structure: The graph to visualize
            step: Optional step information for algorithm visualization
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
            self._figure, self._axes = plt.subplots(figsize=(12, 10))

        state = data_structure.get_state()
        graph_data = state.get("data", {})

        if not graph_data:
            self._axes.text(
                0,
                0,
                "Empty Graph",
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold",
            )
            self._axes.axis("off")
            return

        # Extract graph information
        adjacency_list = graph_data.get("adjacency_list", {})
        vertices = graph_data.get("vertices", [])
        edges = graph_data.get("edges", [])
        is_directed = graph_data.get("directed", False)

        if not vertices:
            self._axes.text(
                0,
                0,
                "Empty Graph",
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold",
            )
            self._axes.axis("off")
            return

        # Calculate node positions
        self._calculate_layout(vertices, edges)

        # Get algorithm state from step
        visited = set(step.get("visited", [])) if step else set()
        current_vertex = step.get("current_vertex", None) if step else None
        queue = step.get("queue", []) if step else []
        stack = step.get("stack", []) if step else []
        traversal_order = step.get("traversal_order", []) if step else []
        path = step.get("path", []) if step else []

        # Draw edges first
        self._draw_edges(edges, is_directed, visited, traversal_order, path)

        # Draw nodes
        self._draw_nodes(
            vertices, visited, current_vertex, queue, stack, traversal_order, path
        )

        # Set axis limits
        if self._node_positions:
            x_coords = [pos[0] for pos in self._node_positions.values()]
            y_coords = [pos[1] for pos in self._node_positions.values()]
            x_margin = max(1, max(x_coords) * 0.2) if x_coords else 2
            y_margin = max(1, max(y_coords) * 0.2) if y_coords else 2

            self._axes.set_xlim(min(x_coords) - x_margin, max(x_coords) + x_margin)
            self._axes.set_ylim(min(y_coords) - y_margin, max(y_coords) + y_margin)
        else:
            self._axes.set_xlim(-2, 2)
            self._axes.set_ylim(-2, 2)

        self._axes.set_aspect("equal")
        self._axes.axis("off")

        # Add title
        ds_type = state.get("type", "Graph")
        title = f"{ds_type} Visualization"
        if step:
            if "algorithm" in step:
                title += f" - {step['algorithm']}"
            if "step_number" in step:
                title += f" (Step {step['step_number']})"
        self._axes.set_title(title, fontsize=14, fontweight="bold", pad=20)

    def _calculate_layout(self, vertices: List[Any], edges: List[Tuple]) -> None:
        """
        Calculate node positions using force-directed layout.

        Args:
            vertices: List of vertices
            edges: List of edges
        """
        import math

        self._node_positions.clear()

        if not vertices:
            return

        num_vertices = len(vertices)

        # Use circular layout as initial positions
        radius = max(3, num_vertices / 2)
        center_x, center_y = 0, 0

        for i, vertex in enumerate(vertices):
            angle = 2 * math.pi * i / num_vertices if num_vertices > 1 else 0
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            self._node_positions[vertex] = (x, y)

        # Simple force-directed iterations (simplified version)
        # In a full implementation, would use more sophisticated force calculations
        for _ in range(50):  # Iterations
            new_positions = {}
            for vertex in vertices:
                x, y = self._node_positions[vertex]

                # Repulsion from other nodes
                fx, fy = 0, 0
                for other_vertex in vertices:
                    if other_vertex == vertex:
                        continue
                    ox, oy = self._node_positions[other_vertex]
                    dx = x - ox
                    dy = y - oy
                    dist = math.sqrt(dx * dx + dy * dy) or 1
                    # Repulsion force
                    force = 0.1 / (dist * dist)
                    fx += force * dx / dist
                    fy += force * dy / dist

                # Attraction to neighbors
                for edge in edges:
                    from_v, to_v, weight = edge[0], edge[1], edge[2] if len(edge) > 2 else None
                    if from_v == vertex and to_v in self._node_positions:
                        ox, oy = self._node_positions[to_v]
                        dx = ox - x
                        dy = oy - y
                        dist = math.sqrt(dx * dx + dy * dy) or 1
                        # Attraction force
                        force = 0.01 * dist
                        fx += force * dx / dist
                        fy += force * dy / dist
                    elif to_v == vertex and from_v in self._node_positions:
                        ox, oy = self._node_positions[from_v]
                        dx = ox - x
                        dy = oy - y
                        dist = math.sqrt(dx * dx + dy * dy) or 1
                        force = 0.01 * dist
                        fx += force * dx / dist
                        fy += force * dy / dist

                # Update position
                new_x = x + fx * 0.1
                new_y = y + fy * 0.1
                new_positions[vertex] = (new_x, new_y)

            self._node_positions.update(new_positions)

    def _draw_edges(
        self,
        edges: List[Tuple],
        is_directed: bool,
        visited: Set[Any],
        traversal_order: List[Any],
        path: List[Any],
    ) -> None:
        """
        Draw graph edges.

        Args:
            edges: List of edges
            is_directed: Whether graph is directed
            visited: Set of visited vertices
            traversal_order: Order of traversal
            path: Current path
        """
        for edge in edges:
            from_v = edge[0]
            to_v = edge[1]
            weight = edge[2] if len(edge) > 2 else None

            if from_v not in self._node_positions or to_v not in self._node_positions:
                continue

            fx, fy = self._node_positions[from_v]
            tx, ty = self._node_positions[to_v]

            # Adjust for node radius
            dx = tx - fx
            dy = ty - fy
            dist = (dx * dx + dy * dy) ** 0.5
            if dist > 0:
                ux = dx / dist
                uy = dy / dist
                start_x = fx + ux * self._node_radius
                start_y = fy + uy * self._node_radius
                end_x = tx - ux * self._node_radius
                end_y = ty - uy * self._node_radius

                # Determine edge color
                edge_color = "gray"
                edge_width = 1
                edge_alpha = 0.5

                if from_v in path and to_v in path:
                    # Edge is on path
                    edge_color = "blue"
                    edge_width = 2.5
                    edge_alpha = 0.8
                elif from_v in visited and to_v in visited:
                    # Both vertices visited
                    edge_color = "green"
                    edge_width = 1.5
                    edge_alpha = 0.6

                # Draw edge
                self._axes.plot(
                    [start_x, end_x],
                    [start_y, end_y],
                    color=edge_color,
                    linewidth=edge_width,
                    alpha=edge_alpha,
                )

                # Draw arrow for directed edges
                if is_directed:
                    arrow_length = 0.3
                    arrow_x = end_x - ux * arrow_length
                    arrow_y = end_y - uy * arrow_length
                    self._axes.annotate(
                        "",
                        xy=(end_x, end_y),
                        xytext=(arrow_x, arrow_y),
                        arrowprops=dict(
                            arrowstyle="->", lw=edge_width, color=edge_color, alpha=edge_alpha
                        ),
                    )

                # Draw weight if present
                if weight is not None:
                    mid_x = (start_x + end_x) / 2
                    mid_y = (start_y + end_y) / 2
                    self._axes.text(
                        mid_x,
                        mid_y,
                        str(weight),
                        ha="center",
                        va="center",
                        fontsize=8,
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7),
                    )

    def _draw_nodes(
        self,
        vertices: List[Any],
        visited: Set[Any],
        current_vertex: Any,
        queue: List[Any],
        stack: List[Any],
        traversal_order: List[Any],
        path: List[Any],
    ) -> None:
        """
        Draw graph nodes with appropriate colors.

        Args:
            vertices: List of vertices
            visited: Set of visited vertices
            current_vertex: Currently processing vertex
            queue: Vertices in queue
            stack: Vertices in stack
            traversal_order: Order of traversal
            path: Current path
        """
        import matplotlib.patches as patches

        for vertex in vertices:
            pos = self._node_positions.get(vertex)
            if pos is None:
                continue

            x, y = pos

            # Determine node color
            color = "lightgray"  # Unvisited
            edge_color = "black"
            edge_width = 2

            if vertex == current_vertex:
                color = "yellow"  # Currently processing
                edge_color = "red"
                edge_width = 3
            elif vertex in path:
                color = "lightblue"  # On path
                edge_color = "blue"
                edge_width = 2.5
            elif vertex in visited:
                color = "lightgreen"  # Visited
                edge_color = "darkgreen"
                edge_width = 2
            elif vertex in queue:
                color = "orange"  # In queue
                edge_color = "darkorange"
                edge_width = 2
            elif vertex in stack:
                color = "pink"  # In stack
                edge_color = "deeppink"
                edge_width = 2

            # Draw node circle
            circle = patches.Circle(
                (x, y),
                self._node_radius,
                linewidth=edge_width,
                edgecolor=edge_color,
                facecolor=color,
            )
            self._axes.add_patch(circle)

            # Add vertex label
            self._axes.text(
                x,
                y,
                str(vertex),
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

            # Add traversal order number if in traversal
            if vertex in traversal_order:
                order = traversal_order.index(vertex) + 1
                self._axes.text(
                    x,
                    y + self._node_radius + 0.2,
                    str(order),
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold",
                    color="blue",
                )

    def visualize_bfs(
        self, data_structure: BaseDataStructure, visited: Set[Any], queue: List[Any], current: Any
    ):
        """
        Visualize BFS state.

        Args:
            data_structure: The graph
            visited: Visited vertices
            queue: Queue contents
            current: Current vertex
        """
        step = {
            "algorithm": "BFS",
            "visited": list(visited),
            "queue": queue,
            "current_vertex": current,
        }
        self.visualize(data_structure, step)

    def visualize_dfs(
        self, data_structure: BaseDataStructure, visited: Set[Any], stack: List[Any], current: Any
    ):
        """
        Visualize DFS state.

        Args:
            data_structure: The graph
            visited: Visited vertices
            stack: Stack contents
            current: Current vertex
        """
        step = {
            "algorithm": "DFS",
            "visited": list(visited),
            "stack": stack,
            "current_vertex": current,
        }
        self.visualize(data_structure, step)

    def visualize_path(self, data_structure: BaseDataStructure, path: List[Any]):
        """
        Visualize a path in the graph.

        Args:
            data_structure: The graph
            path: List of vertices in path
        """
        step = {"algorithm": "Path Finding", "path": path}
        self.visualize(data_structure, step)

    def animate(self, steps: List[Dict[str, Any]]):
        """
        Animate through a series of graph algorithm steps.

        Args:
            steps: List of step dictionaries
        """
        import matplotlib.animation as animation
        import matplotlib.pyplot as plt

        if not steps:
            return

        fig, ax = plt.subplots(figsize=(12, 10))

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

