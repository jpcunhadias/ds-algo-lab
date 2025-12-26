"""
Visualization Module
Visualization engine for data structures and algorithms.
"""

from .base import BaseVisualizer, BaseDataStructure, BaseAlgorithm
from .ds_visualizer import DataStructureVisualizer
from .algo_visualizer import AlgorithmVisualizer

# Lazy imports to avoid circular dependencies
# These modules import algorithms/data structures which can create cycles
__all__ = [
    'BaseVisualizer',
    'BaseDataStructure',
    'BaseAlgorithm',
    'DataStructureVisualizer',
    'AlgorithmVisualizer',
]


def __getattr__(name):
    """Lazy import for modules that may cause circular dependencies."""
    if name == 'InteractiveControls':
        from .interactive_controls import InteractiveControls
        return InteractiveControls
    elif name == 'ComparisonViewer':
        from .comparison_viewer import ComparisonViewer
        return ComparisonViewer
    elif name == 'TreeVisualizer':
        from .tree_visualizer import TreeVisualizer
        return TreeVisualizer
    elif name == 'GraphVisualizer':
        from .graph_visualizer import GraphVisualizer
        return GraphVisualizer
    elif name == 'HashTableVisualizer':
        from .hash_table_visualizer import HashTableVisualizer
        return HashTableVisualizer
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

