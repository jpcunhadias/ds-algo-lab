"""
Graph data structure implementation.
A graph with adjacency list representation and visualization hooks.
"""

from typing import Any, Optional, List, Dict, Set, Tuple
from ..visualization.base import BaseDataStructure


class Graph(BaseDataStructure):
    """
    Graph implementation with visualization support.
    Uses adjacency list representation.
    Supports both directed and undirected graphs.
    """

    def __init__(self, directed: bool = False, initial_vertices: Optional[List[Any]] = None):
        """
        Initialize the graph.

        Args:
            directed: Whether the graph is directed (default: False)
            initial_vertices: Optional initial vertices to add
        """
        super().__init__()
        self._adjacency_list: Dict[Any, List[Tuple[Any, Optional[float]]]] = {}
        self._directed = directed
        self._size = 0

        # Add initial vertices
        if initial_vertices:
            for vertex in initial_vertices:
                self.add_vertex(vertex)

        # Notify visualizer of initialization
        self._notify_visualizer('init', {
            'data_structure': self,
            'directed': directed,
            'initial_vertices': initial_vertices or []
        })

    def add_vertex(self, vertex: Any) -> None:
        """
        Add a vertex to the graph.

        Args:
            vertex: The vertex to add
        """
        if vertex not in self._adjacency_list:
            self._adjacency_list[vertex] = []
            self._size += 1
            self._notify_visualizer('add_vertex', {
                'data_structure': self,
                'vertex': vertex
            })

    def remove_vertex(self, vertex: Any) -> bool:
        """
        Remove a vertex from the graph.

        Args:
            vertex: The vertex to remove

        Returns:
            True if vertex was removed, False if not found
        """
        if vertex not in self._adjacency_list:
            return False

        # Remove all edges connected to this vertex
        neighbors = self._adjacency_list[vertex].copy()
        for neighbor, weight in neighbors:
            self.remove_edge(vertex, neighbor)

        # Remove vertex from adjacency lists of other vertices
        for v in self._adjacency_list:
            self._adjacency_list[v] = [
                (n, w) for n, w in self._adjacency_list[v] if n != vertex
            ]

        # Remove vertex
        del self._adjacency_list[vertex]
        self._size -= 1

        self._notify_visualizer('remove_vertex', {
            'data_structure': self,
            'vertex': vertex
        })
        return True

    def add_edge(self, from_vertex: Any, to_vertex: Any, weight: Optional[float] = None) -> None:
        """
        Add an edge to the graph.

        Args:
            from_vertex: Source vertex
            to_vertex: Destination vertex
            weight: Optional edge weight
        """
        # Add vertices if they don't exist
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)

        # Add edge
        if (to_vertex, weight) not in self._adjacency_list[from_vertex]:
            self._adjacency_list[from_vertex].append((to_vertex, weight))

        # If undirected, add reverse edge
        if not self._directed:
            if (from_vertex, weight) not in self._adjacency_list[to_vertex]:
                self._adjacency_list[to_vertex].append((from_vertex, weight))

        self._notify_visualizer('add_edge', {
            'data_structure': self,
            'from_vertex': from_vertex,
            'to_vertex': to_vertex,
            'weight': weight
        })

    def remove_edge(self, from_vertex: Any, to_vertex: Any) -> bool:
        """
        Remove an edge from the graph.

        Args:
            from_vertex: Source vertex
            to_vertex: Destination vertex

        Returns:
            True if edge was removed, False if not found
        """
        if from_vertex not in self._adjacency_list:
            return False

        # Remove edge
        original_length = len(self._adjacency_list[from_vertex])
        self._adjacency_list[from_vertex] = [
            (v, w) for v, w in self._adjacency_list[from_vertex] if v != to_vertex
        ]
        removed = len(self._adjacency_list[from_vertex]) < original_length

        # If undirected, remove reverse edge
        if not self._directed and to_vertex in self._adjacency_list:
            self._adjacency_list[to_vertex] = [
                (v, w) for v, w in self._adjacency_list[to_vertex] if v != from_vertex
            ]

        if removed:
            self._notify_visualizer('remove_edge', {
                'data_structure': self,
                'from_vertex': from_vertex,
                'to_vertex': to_vertex
            })

        return removed

    def get_neighbors(self, vertex: Any) -> List[Tuple[Any, Optional[float]]]:
        """
        Get neighbors of a vertex.

        Args:
            vertex: The vertex

        Returns:
            List of (neighbor, weight) tuples
        """
        return self._adjacency_list.get(vertex, []).copy()

    def has_edge(self, from_vertex: Any, to_vertex: Any) -> bool:
        """
        Check if an edge exists.

        Args:
            from_vertex: Source vertex
            to_vertex: Destination vertex

        Returns:
            True if edge exists, False otherwise
        """
        if from_vertex not in self._adjacency_list:
            return False
        return any(v == to_vertex for v, _ in self._adjacency_list[from_vertex])

    def get_vertices(self) -> List[Any]:
        """
        Get all vertices in the graph.

        Returns:
            List of vertices
        """
        return list(self._adjacency_list.keys())

    def get_edges(self) -> List[Tuple[Any, Any, Optional[float]]]:
        """
        Get all edges in the graph.

        Returns:
            List of (from_vertex, to_vertex, weight) tuples
        """
        edges = []
        visited_edges = set()

        for from_vertex in self._adjacency_list:
            for to_vertex, weight in self._adjacency_list[from_vertex]:
                # For undirected graphs, avoid duplicate edges
                if not self._directed:
                    edge_key = tuple(sorted([from_vertex, to_vertex]))
                    if edge_key in visited_edges:
                        continue
                    visited_edges.add(edge_key)

                edges.append((from_vertex, to_vertex, weight))

        return edges

    def is_directed(self) -> bool:
        """
        Check if the graph is directed.

        Returns:
            True if directed, False otherwise
        """
        return self._directed

    def _get_internal_state(self) -> Dict[str, Any]:
        """
        Get the internal state representation.

        Returns:
            Dictionary representation of the graph
        """
        return {
            'directed': self._directed,
            'adjacency_list': {
                str(k): [(str(v), w) for v, w in neighbors]
                for k, neighbors in self._adjacency_list.items()
            },
            'vertices': [str(v) for v in self._adjacency_list.keys()],
            'edges': [
                (str(f), str(t), w) for f, t, w in self.get_edges()
            ]
        }

    def __len__(self) -> int:
        """Return the number of vertices."""
        return self._size

    def __repr__(self) -> str:
        """String representation of the graph."""
        graph_type = "Directed" if self._directed else "Undirected"
        return f"Graph({graph_type}, vertices={self._size}, edges={len(self.get_edges())})"

