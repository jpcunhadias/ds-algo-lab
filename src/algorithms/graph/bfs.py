"""
Breadth-First Search (BFS) algorithm implementation with step tracking.
"""

from typing import List, Dict, Any, Optional, Set
from ...visualization.base import BaseAlgorithm
from ...data_structures.graph import Graph


class BFS(BaseAlgorithm):
    """
    Breadth-First Search algorithm with visualization support.
    """

    def __init__(self):
        """Initialize the BFS algorithm."""
        super().__init__()
        self._name = "Breadth-First Search"

    def _run(self, data_structure):
        """
        Run the BFS algorithm.

        Args:
            data_structure: Graph to traverse

        Yields:
            Dictionary containing step information
        """
        # Get start vertex from instance variable
        start_vertex = getattr(self, '_start_vertex', None)

        if start_vertex is None or not isinstance(data_structure, Graph):
            return

        graph = data_structure
        step_number = 0

        # Initialize
        visited: Set[Any] = set()
        queue: List[Any] = [start_vertex]
        visited.add(start_vertex)
        traversal_order: List[Any] = []

        step_number += 1
        yield {
            'algorithm': self._name,
            'step_number': step_number,
            'description': f'Starting BFS from vertex {start_vertex}',
            'data_structure': graph,
            'start_vertex': start_vertex,
            'current_vertex': start_vertex,
            'visited': list(visited.copy()),
            'queue': queue.copy(),
            'traversal_order': traversal_order.copy(),
            'phase': 'initialization'
        }

        while queue:
            # Dequeue a vertex
            current = queue.pop(0)
            traversal_order.append(current)

            step_number += 1
            yield {
                'algorithm': self._name,
                'step_number': step_number,
                'description': f'Processing vertex {current}',
                'data_structure': graph,
                'start_vertex': start_vertex,
                'current_vertex': current,
                'visited': list(visited.copy()),
                'queue': queue.copy(),
                'traversal_order': traversal_order.copy(),
                'phase': 'processing'
            }

            # Get neighbors
            neighbors = graph.get_neighbors(current)

            step_number += 1
            yield {
                'algorithm': self._name,
                'step_number': step_number,
                'description': f'Exploring neighbors of {current}: {[n[0] for n in neighbors]}',
                'data_structure': graph,
                'start_vertex': start_vertex,
                'current_vertex': current,
                'visited': list(visited.copy()),
                'queue': queue.copy(),
                'traversal_order': traversal_order.copy(),
                'neighbors': [n[0] for n in neighbors],
                'phase': 'exploring'
            }

            # Visit unvisited neighbors
            for neighbor, weight in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

                    step_number += 1
                    yield {
                        'algorithm': self._name,
                        'step_number': step_number,
                        'description': f'Discovered vertex {neighbor}, adding to queue',
                        'data_structure': graph,
                        'start_vertex': start_vertex,
                        'current_vertex': current,
                        'visited': list(visited.copy()),
                        'queue': queue.copy(),
                        'traversal_order': traversal_order.copy(),
                        'discovered_vertex': neighbor,
                        'phase': 'discovery'
                    }

        # Final step
        step_number += 1
        yield {
            'algorithm': self._name,
            'step_number': step_number,
            'description': f'BFS complete. Traversal order: {traversal_order}',
            'data_structure': graph,
            'start_vertex': start_vertex,
            'current_vertex': None,
            'visited': list(visited.copy()),
            'queue': [],
            'traversal_order': traversal_order.copy(),
            'phase': 'complete'
        }

    def execute(self, data_structure, start_vertex: Any, visualize: bool = True) -> List[Dict[str, Any]]:
        """
        Execute BFS from a start vertex.

        Args:
            data_structure: The graph to traverse
            start_vertex: The starting vertex
            visualize: Whether to visualize during execution

        Returns:
            List of execution steps
        """
        self._start_vertex = start_vertex
        return super().execute(data_structure, visualize)

