"""
Matplotlib Renderer
Matplotlib implementation of the renderer interface.
"""

from typing import Any, Dict, Optional
import matplotlib.pyplot as plt
from .base_renderer import BaseRenderer
from ..base import BaseDataStructure


class MatplotlibRenderer(BaseRenderer):
    """
    Matplotlib-based renderer implementation.
    Wraps existing matplotlib visualization code.
    """

    def __init__(self):
        """Initialize matplotlib renderer."""
        self._figure = None
        self._axes = None

    def render_array(
        self,
        data_structure: BaseDataStructure,
        step: Optional[Dict[str, Any]] = None,
        ax=None,
        fig=None,
    ) -> None:
        """
        Render an array visualization using matplotlib.

        Args:
            data_structure: Array data structure
            step: Optional step information
            ax: Optional axes to render on
            fig: Optional figure
        """
        from ..ds_visualizer import DataStructureVisualizer

        visualizer = DataStructureVisualizer()
        visualizer.visualize(data_structure, step)
        if ax is not None:
            self._axes = ax
            self._figure = fig

    def render_tree(
        self,
        data_structure: BaseDataStructure,
        step: Optional[Dict[str, Any]] = None,
        ax=None,
        fig=None,
    ) -> None:
        """
        Render a tree visualization using matplotlib.

        Args:
            data_structure: Tree data structure
            step: Optional step information
            ax: Optional axes to render on
            fig: Optional figure
        """
        from ..tree_visualizer import TreeVisualizer

        visualizer = TreeVisualizer()
        visualizer.visualize(data_structure, step, ax=ax, fig=fig)
        if ax is not None:
            self._axes = ax
            self._figure = fig

    def render_graph(
        self,
        data_structure: BaseDataStructure,
        step: Optional[Dict[str, Any]] = None,
        ax=None,
        fig=None,
    ) -> None:
        """
        Render a graph visualization using matplotlib.

        Args:
            data_structure: Graph data structure
            step: Optional step information
            ax: Optional axes to render on
            fig: Optional figure
        """
        from ..graph_visualizer import GraphVisualizer

        visualizer = GraphVisualizer()
        visualizer.visualize(data_structure, step, ax=ax, fig=fig)
        if ax is not None:
            self._axes = ax
            self._figure = fig

    def render_hash_table(
        self,
        data_structure: BaseDataStructure,
        step: Optional[Dict[str, Any]] = None,
        ax=None,
        fig=None,
    ) -> None:
        """
        Render a hash table visualization using matplotlib.

        Args:
            data_structure: Hash table data structure
            step: Optional step information
            ax: Optional axes to render on
            fig: Optional figure
        """
        from ..hash_table_visualizer import HashTableVisualizer

        visualizer = HashTableVisualizer()
        visualizer.visualize(data_structure, step, ax=ax, fig=fig)
        if ax is not None:
            self._axes = ax
            self._figure = fig

    def create_figure(self, figsize: tuple = (12, 6)):
        """
        Create a new matplotlib figure.

        Args:
            figsize: Figure size tuple

        Returns:
            Figure and axes tuple
        """
        self._figure, self._axes = plt.subplots(figsize=figsize)
        return self._figure, self._axes

    def show(self) -> None:
        """Display the matplotlib visualization."""
        if self._figure:
            plt.show()
        else:
            plt.show()

    def save(self, filename: str) -> None:
        """
        Save the matplotlib visualization to a file.

        Args:
            filename: Output filename
        """
        if self._figure:
            self._figure.savefig(filename, bbox_inches="tight")
        else:
            plt.savefig(filename, bbox_inches="tight")

