"""
Base Renderer Interface
Abstract interface for visualization renderers.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..base import BaseDataStructure


class BaseRenderer(ABC):
    """
    Abstract base class for visualization renderers.
    Provides interface for different rendering backends (matplotlib, plotly, etc.).
    """

    @abstractmethod
    def render_array(
        self,
        data_structure: BaseDataStructure,
        step: Optional[Dict[str, Any]] = None,
        ax=None,
        fig=None,
    ) -> None:
        """
        Render an array visualization.

        Args:
            data_structure: Array data structure
            step: Optional step information
            ax: Optional axes to render on
            fig: Optional figure
        """
        pass

    @abstractmethod
    def render_tree(
        self,
        data_structure: BaseDataStructure,
        step: Optional[Dict[str, Any]] = None,
        ax=None,
        fig=None,
    ) -> None:
        """
        Render a tree visualization.

        Args:
            data_structure: Tree data structure
            step: Optional step information
            ax: Optional axes to render on
            fig: Optional figure
        """
        pass

    @abstractmethod
    def render_graph(
        self,
        data_structure: BaseDataStructure,
        step: Optional[Dict[str, Any]] = None,
        ax=None,
        fig=None,
    ) -> None:
        """
        Render a graph visualization.

        Args:
            data_structure: Graph data structure
            step: Optional step information
            ax: Optional axes to render on
            fig: Optional figure
        """
        pass

    @abstractmethod
    def render_hash_table(
        self,
        data_structure: BaseDataStructure,
        step: Optional[Dict[str, Any]] = None,
        ax=None,
        fig=None,
    ) -> None:
        """
        Render a hash table visualization.

        Args:
            data_structure: Hash table data structure
            step: Optional step information
            ax: Optional axes to render on
            fig: Optional figure
        """
        pass

    @abstractmethod
    def create_figure(self, figsize: tuple = (12, 6)):
        """
        Create a new figure.

        Args:
            figsize: Figure size tuple

        Returns:
            Figure and axes tuple
        """
        pass

    @abstractmethod
    def show(self) -> None:
        """Display the visualization."""
        pass

    @abstractmethod
    def save(self, filename: str) -> None:
        """
        Save the visualization to a file.

        Args:
            filename: Output filename
        """
        pass

