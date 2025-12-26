"""
Interactive playground system for exploring algorithms visually.
"""

from .base import Playground, InputGenerator
from .input_builder import InputBuilder

# Lazy imports to avoid circular dependencies
__all__ = ['Playground', 'InputGenerator', 'InputBuilder']


def __getattr__(name):
    """Lazy import for playground classes to avoid circular dependencies."""
    if name == 'SortingPlayground':
        from .sorting_playground import SortingPlayground
        return SortingPlayground
    elif name == 'SearchingPlayground':
        from .searching_playground import SearchingPlayground
        return SearchingPlayground
    elif name == 'TreePlayground':
        from .tree_playground import TreePlayground
        return TreePlayground
    elif name == 'GraphPlayground':
        from .graph_playground import GraphPlayground
        return GraphPlayground
    elif name == 'HashTablePlayground':
        from .hash_table_playground import HashTablePlayground
        return HashTablePlayground
    elif name == 'UnifiedDSPlayground':
        from .ds_playground import UnifiedDSPlayground
        return UnifiedDSPlayground
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

