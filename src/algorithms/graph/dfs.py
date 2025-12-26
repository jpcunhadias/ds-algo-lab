"""
Depth-First Search (DFS) algorithm implementation with step tracking.
"""

from typing import List, Dict, Any, Optional, Set
from ...visualization.base import BaseAlgorithm
from ...data_structures.graph import Graph


class DFS(BaseAlgorithm):
    """
    Depth-First Search algorithm with visualization support.
    """

    def __init__(self):
        """Initialize the DFS algorithm."""
        super().__init__()
        self._name = "Depth-First Search"

    def _run(self, data_structure):
        """
        Run the DFS algorithm.

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
        stack: List[Any] = [start_vertex]
        traversal_order: List[Any] = []
        path: List[Any] = []

        step_number += 1
        yield {
            'algorithm': self._name,
            'step_number': step_number,
            'description': f'Starting DFS from vertex {start_vertex}',
            'data_structure': graph,
            'start_vertex': start_vertex,
            'current_vertex': start_vertex,
            'visited': list(visited.copy()),
            'stack': stack.copy(),
            'traversal_order': traversal_order.copy(),
            'path': path.copy(),
            'phase': 'initialization'
        }

        while stack:
            # Pop a vertex from stack
            current = stack.pop()
            path.append(current)

            if current not in visited:
                visited.add(current)
                traversal_order.append(current)

                step_number += 1
                yield {
                    'algorithm': self._name,
                    'step_number': step_number,
                    'description': f'Visiting vertex {current}',
                    'data_structure': graph,
                    'start_vertex': start_vertex,
                    'current_vertex': current,
                    'visited': list(visited.copy()),
                    'stack': stack.copy(),
                    'traversal_order': traversal_order.copy(),
                    'path': path.copy(),
                    'phase': 'visiting'
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
                    'stack': stack.copy(),
                    'traversal_order': traversal_order.copy(),
                    'path': path.copy(),
                    'neighbors': [n[0] for n in neighbors],
                    'phase': 'exploring'
                }

                # Push unvisited neighbors onto stack
                for neighbor, weight in reversed(neighbors):  # Reverse to maintain left-to-right order
                    if neighbor not in visited:
                        stack.append(neighbor)

                        step_number += 1
                        yield {
                            'algorithm': self._name,
                            'step_number': step_number,
                            'description': f'Pushing unvisited neighbor {neighbor} onto stack',
                            'data_structure': graph,
                            'start_vertex': start_vertex,
                            'current_vertex': current,
                            'visited': list(visited.copy()),
                            'stack': stack.copy(),
                            'traversal_order': traversal_order.copy(),
                            'path': path.copy(),
                            'discovered_vertex': neighbor,
                            'phase': 'discovery'
                        }
            else:
                # Backtracking
                step_number += 1
                yield {
                    'algorithm': self._name,
                    'step_number': step_number,
                    'description': f'Backtracking from {current} (already visited)',
                    'data_structure': graph,
                    'start_vertex': start_vertex,
                    'current_vertex': current,
                    'visited': list(visited.copy()),
                    'stack': stack.copy(),
                    'traversal_order': traversal_order.copy(),
                    'path': path.copy(),
                    'phase': 'backtracking'
                }

                # Remove from path when backtracking
                if path and path[-1] == current:
                    path.pop()

        # Final step
        step_number += 1
        yield {
            'algorithm': self._name,
            'step_number': step_number,
            'description': f'DFS complete. Traversal order: {traversal_order}',
            'data_structure': graph,
            'start_vertex': start_vertex,
            'current_vertex': None,
            'visited': list(visited.copy()),
            'stack': [],
            'traversal_order': traversal_order.copy(),
            'path': [],
            'phase': 'complete'
        }

    def execute(self, data_structure, start_vertex: Any, visualize: bool = True) -> List[Dict[str, Any]]:
        """
        Execute DFS from a start vertex.

        Args:
            data_structure: The graph to traverse
            start_vertex: The starting vertex
            visualize: Whether to visualize during execution

        Returns:
            List of execution steps
        """
        self._start_vertex = start_vertex
        return super().execute(data_structure, visualize)

