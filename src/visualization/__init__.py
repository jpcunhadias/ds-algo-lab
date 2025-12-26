"""
Visualization Module
Visualization engine for data structures and algorithms.
"""

from .algo_visualizer import AlgorithmVisualizer
from .base import BaseAlgorithm, BaseDataStructure, BaseVisualizer
from .ds_visualizer import DataStructureVisualizer

# Lazy imports to avoid circular dependencies
# These modules import algorithms/data structures which can create cycles
__all__ = [
    "BaseVisualizer",
    "BaseDataStructure",
    "BaseAlgorithm",
    "DataStructureVisualizer",
    "AlgorithmVisualizer",
]


def __getattr__(name):
    """Lazy import for modules that may cause circular dependencies."""
    if name == "InteractiveControls":
        from .interactive_controls import InteractiveControls

        return InteractiveControls
    elif name == "ComparisonViewer":
        from .comparison_viewer import ComparisonViewer

        return ComparisonViewer
    elif name == "TreeVisualizer":
        from .tree_visualizer import TreeVisualizer

        return TreeVisualizer
    elif name == "GraphVisualizer":
        from .graph_visualizer import GraphVisualizer

        return GraphVisualizer
    elif name == "HashTableVisualizer":
        from .hash_table_visualizer import HashTableVisualizer

        return HashTableVisualizer
    elif name == "ThemeManager":
        from .theme_manager import Theme, ThemeManager

        return ThemeManager
    elif name == "Theme":
        from .theme_manager import Theme

        return Theme
    elif name == "CodeOverlay":
        from .code_overlay import CodeOverlay

        return CodeOverlay
    elif name == "VariableTracker":
        from .variable_tracker import VariableTracker

        return VariableTracker
    elif name == "PerformancePanel":
        from .performance_panel import PerformanceMetrics, PerformancePanel

        return PerformancePanel
    elif name == "InsightsPanel":
        from .insights_panel import InsightsPanel

        return InsightsPanel
    elif name == "AnimationEngine":
        from .animation_engine import AnimationEngine

        return AnimationEngine
    elif name == "ComplexityViewer":
        from .complexity_viewer import ComplexityViewer

        return ComplexityViewer
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
