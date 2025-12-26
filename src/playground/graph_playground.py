"""
Graph algorithm playground for interactive exploration.
"""

from typing import List, Dict, Any, Optional, Set
from .base import Playground


class GraphPlayground(Playground):
    """
    Interactive playground for exploring graph data structures and algorithms.
    """

    def __init__(self, directed: bool = False):
        """
        Initialize graph playground.

        Args:
            directed: Whether graph is directed
        """
        super().__init__(f"Graph Playground ({'Directed' if directed else 'Undirected'})")
        self.directed = directed
        from ..data_structures.graph import Graph

        self.graph = Graph(directed=directed)

    def set_input(self, data: List[Any], show_initialization: bool = True) -> None:
        """
        Set input vertices.

        Args:
            data: List of vertex values
            show_initialization: Whether to show initialization visualization (default: True)
        """
        self._initialization_steps = []
        step_counter = 0

        for vertex in data:
            # Get vertex addition steps
            steps = self.add_vertex(vertex)
            # Renumber steps to be sequential across all additions
            # Store a snapshot of graph state for each step
            for step in steps:
                step_counter += 1
                step["step_number"] = step_counter
                step["initialization"] = True
                # Store snapshot of graph state at this point
                if "data_structure" in step:
                    graph_state = step["data_structure"].get_state()
                    step["graph_state_snapshot"] = graph_state
                self._initialization_steps.append(step)

        # Add final state step
        if len(self._initialization_steps) > 0:
            step_counter += 1
            self._initialization_steps.append({
                "operation": "initialization_complete",
                "step_number": step_counter,
                "description": f"Graph construction complete. Added {len(data)} vertices.",
                "data_structure": self.graph,
                "current_vertex": None,
                "initialization": True,
            })

        if show_initialization and len(self._initialization_steps) > 0:
            self.visualize_initialization(interactive=True, auto_show=True)

    def add_vertex(self, vertex: Any) -> List[Dict[str, Any]]:
        """
        Add a vertex to the graph.

        Args:
            vertex: Vertex to add

        Returns:
            List of operation steps
        """
        steps = []
        step_number = 0

        step_number += 1
        steps.append(
            {
                "operation": "add_vertex",
                "step_number": step_number,
                "description": f"Adding vertex {vertex}",
                "data_structure": self.graph,
                "current_vertex": vertex,
            }
        )

        self.graph.add_vertex(vertex)

        step_number += 1
        steps.append(
            {
                "operation": "add_vertex",
                "step_number": step_number,
                "description": f"Added vertex {vertex}",
                "data_structure": self.graph,
                "current_vertex": None,
            }
        )

        return steps

    def add_edge(self, from_vertex: Any, to_vertex: Any, weight: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Add an edge to the graph.

        Args:
            from_vertex: Source vertex
            to_vertex: Destination vertex
            weight: Optional edge weight

        Returns:
            List of operation steps
        """
        steps = []
        step_number = 0

        step_number += 1
        steps.append(
            {
                "operation": "add_edge",
                "step_number": step_number,
                "description": f"Adding edge from {from_vertex} to {to_vertex}",
                "data_structure": self.graph,
                "current_vertex": from_vertex,
                "path": [from_vertex, to_vertex],
            }
        )

        self.graph.add_edge(from_vertex, to_vertex, weight)

        step_number += 1
        steps.append(
            {
                "operation": "add_edge",
                "step_number": step_number,
                "description": f"Added edge from {from_vertex} to {to_vertex}",
                "data_structure": self.graph,
                "current_vertex": None,
            }
        )

        return steps

    def run_bfs(self, start_vertex: Any) -> List[Dict[str, Any]]:
        """
        Run BFS algorithm.

        Args:
            start_vertex: Starting vertex

        Returns:
            List of algorithm steps
        """
        from ..algorithms.graph.bfs import BFS

        bfs = BFS()
        steps = bfs.execute(self.graph, start_vertex, visualize=False)
        return steps

    def run_dfs(self, start_vertex: Any) -> List[Dict[str, Any]]:
        """
        Run DFS algorithm.

        Args:
            start_vertex: Starting vertex

        Returns:
            List of algorithm steps
        """
        from ..algorithms.graph.dfs import DFS

        dfs = DFS()
        steps = dfs.execute(self.graph, start_vertex, visualize=False)
        return steps

    def visualize_initialization(self, interactive: bool = True, auto_show: bool = True) -> None:
        """
        Visualize how input data was transformed into the graph structure.

        Shows step-by-step vertex addition process.

        Args:
            interactive: Whether to use interactive controls (True) or animated playback (False)
            auto_show: Whether to automatically show the visualization (for CLI integration)
        """
        if self._initialization_steps is None or len(self._initialization_steps) == 0:
            print("No initialization steps available. Graph may not have been initialized with input data.")
            return

        print(f"\nBuilding {'directed' if self.directed else 'undirected'} graph from input...")
        print(f"Showing {len(self._initialization_steps)} initialization steps\n")

        self.visualize(self._initialization_steps, interactive=interactive)

    def visualize(self, steps: List[Dict[str, Any]], interactive: bool = True) -> None:
        """
        Visualize graph operations.

        Args:
            steps: List of operation steps
            interactive: Whether to use interactive controls
        """
        if not steps:
            print("No steps to visualize")
            return

        from ..visualization.graph_visualizer import GraphVisualizer

        visualizer = GraphVisualizer()

        if interactive:
            from ..visualization.interactive_controls import InteractiveControls

            controls = InteractiveControls(steps, visualizer)
            controls.show()
        else:
            visualizer.animate(steps)

    def run_algorithm(self, algorithm_name: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Run a graph algorithm.

        Args:
            algorithm_name: Algorithm name ('bfs', 'dfs')
            **kwargs: Algorithm-specific parameters

        Returns:
            List of algorithm steps
        """
        if algorithm_name == "bfs":
            start_vertex = kwargs.get("start_vertex")
            if start_vertex is None:
                raise ValueError("BFS requires 'start_vertex' parameter")
            return self.run_bfs(start_vertex)
        elif algorithm_name == "dfs":
            start_vertex = kwargs.get("start_vertex")
            if start_vertex is None:
                raise ValueError("DFS requires 'start_vertex' parameter")
            return self.run_dfs(start_vertex)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")

    def get_available_algorithms(self) -> List[str]:
        """
        Get list of available algorithms.

        Returns:
            List of algorithm names
        """
        return ["bfs", "dfs"]

    def demo(self, algorithm: str = "bfs", start_vertex: Optional[Any] = None) -> None:
        """
        Run a quick demonstration.

        Args:
            algorithm: Algorithm to demonstrate ('bfs' or 'dfs')
            start_vertex: Starting vertex (first vertex if None)
        """
        # Create a sample graph
        vertices = ["A", "B", "C", "D", "E"]
        edges = [
            ("A", "B"),
            ("A", "C"),
            ("B", "D"),
            ("C", "D"),
            ("D", "E"),
        ]

        print(f"Creating {'directed' if self.directed else 'undirected'} graph")
        print(f"Vertices: {vertices}")
        print(f"Edges: {edges}")

        # Add vertices and edges
        for vertex in vertices:
            self.graph.add_vertex(vertex)
        for from_v, to_v in edges:
            self.graph.add_edge(from_v, to_v)

        if start_vertex is None:
            start_vertex = vertices[0]

        print(f"\nRunning {algorithm.upper()} from vertex {start_vertex}")

        # Run algorithm
        if algorithm == "bfs":
            steps = self.run_bfs(start_vertex)
        elif algorithm == "dfs":
            steps = self.run_dfs(start_vertex)
        else:
            print(f"Unknown algorithm: {algorithm}")
            return

        print(f"Total steps: {len(steps)}")

        # Visualize
        self.visualize(steps, interactive=True)

