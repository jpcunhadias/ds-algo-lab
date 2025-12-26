"""
Theme Manager
Provides multiple color themes for visualizations with consistent color coding.
"""

from typing import Dict, Any, Optional
from enum import Enum


class Theme(Enum):
    """Available theme options."""
    LIGHT = "light"
    DARK = "dark"
    HIGH_CONTRAST = "high_contrast"
    COLORBLIND_FRIENDLY = "colorblind_friendly"


class ThemeManager:
    """
    Manages color themes for visualizations.
    Provides consistent color coding across all visualizations.
    """

    def __init__(self, theme: Theme = Theme.LIGHT):
        """
        Initialize theme manager.

        Args:
            theme: Theme to use (default: LIGHT)
        """
        self._theme = theme
        self._themes = self._initialize_themes()

    def _initialize_themes(self) -> Dict[str, Dict[str, Any]]:
        """Initialize all available themes."""
        return {
            Theme.LIGHT.value: {
                "background": "white",
                "text": "black",
                "grid": "lightgray",
                "array": {
                    "normal": "#E3F2FD",  # Light blue
                    "comparing": "#FFF9C4",  # Light yellow
                    "swapping": "#FFCDD2",  # Light red
                    "sorted": "#C8E6C9",  # Light green
                    "current": "#FFE0B2",  # Light orange
                    "highlighted": "#FFCCBC",  # Light orange-red
                    "edge": "black",
                    "text": "black",
                },
                "tree": {
                    "node": "#E1F5FE",  # Light cyan
                    "node_highlighted": "#FFF9C4",  # Light yellow
                    "node_current": "#FFE0B2",  # Light orange
                    "edge": "#424242",  # Dark gray
                    "text": "black",
                },
                "graph": {
                    "vertex": "#BBDEFB",  # Light blue
                    "vertex_visited": "#C8E6C9",  # Light green
                    "vertex_current": "#FFE0B2",  # Light orange
                    "edge": "#757575",  # Medium gray
                    "edge_highlighted": "#F44336",  # Red
                    "text": "black",
                },
                "hash_table": {
                    "bucket": "#F5F5F5",  # Light gray
                    "bucket_highlighted": "#FFF9C4",  # Light yellow
                    "item": "#E3F2FD",  # Light blue
                    "item_highlighted": "#FFE0B2",  # Light orange
                    "edge": "black",
                    "text": "black",
                },
            },
            Theme.DARK.value: {
                "background": "#1E1E1E",  # Dark gray
                "text": "#E0E0E0",  # Light gray
                "grid": "#424242",  # Medium gray
                "array": {
                    "normal": "#1565C0",  # Dark blue
                    "comparing": "#F9A825",  # Dark yellow
                    "swapping": "#C62828",  # Dark red
                    "sorted": "#2E7D32",  # Dark green
                    "current": "#E65100",  # Dark orange
                    "highlighted": "#D84315",  # Dark orange-red
                    "edge": "#E0E0E0",  # Light gray
                    "text": "#E0E0E0",  # Light gray
                },
                "tree": {
                    "node": "#0277BD",  # Dark cyan-blue
                    "node_highlighted": "#F9A825",  # Dark yellow
                    "node_current": "#E65100",  # Dark orange
                    "edge": "#BDBDBD",  # Light gray
                    "text": "#E0E0E0",  # Light gray
                },
                "graph": {
                    "vertex": "#1565C0",  # Dark blue
                    "vertex_visited": "#2E7D32",  # Dark green
                    "vertex_current": "#E65100",  # Dark orange
                    "edge": "#757575",  # Medium gray
                    "edge_highlighted": "#EF5350",  # Light red
                    "text": "#E0E0E0",  # Light gray
                },
                "hash_table": {
                    "bucket": "#424242",  # Medium gray
                    "bucket_highlighted": "#F9A825",  # Dark yellow
                    "item": "#1565C0",  # Dark blue
                    "item_highlighted": "#E65100",  # Dark orange
                    "edge": "#E0E0E0",  # Light gray
                    "text": "#E0E0E0",  # Light gray
                },
            },
            Theme.HIGH_CONTRAST.value: {
                "background": "white",
                "text": "black",
                "grid": "#000000",  # Black
                "array": {
                    "normal": "#FFFFFF",  # White
                    "comparing": "#FFFF00",  # Bright yellow
                    "swapping": "#FF0000",  # Bright red
                    "sorted": "#00FF00",  # Bright green
                    "current": "#FF8800",  # Bright orange
                    "highlighted": "#FF00FF",  # Magenta
                    "edge": "#000000",  # Black
                    "text": "#000000",  # Black
                },
                "tree": {
                    "node": "#FFFFFF",  # White
                    "node_highlighted": "#FFFF00",  # Bright yellow
                    "node_current": "#FF8800",  # Bright orange
                    "edge": "#000000",  # Black
                    "text": "#000000",  # Black
                },
                "graph": {
                    "vertex": "#FFFFFF",  # White
                    "vertex_visited": "#00FF00",  # Bright green
                    "vertex_current": "#FF8800",  # Bright orange
                    "edge": "#000000",  # Black
                    "edge_highlighted": "#FF0000",  # Bright red
                    "text": "#000000",  # Black
                },
                "hash_table": {
                    "bucket": "#FFFFFF",  # White
                    "bucket_highlighted": "#FFFF00",  # Bright yellow
                    "item": "#FFFFFF",  # White
                    "item_highlighted": "#FF8800",  # Bright orange
                    "edge": "#000000",  # Black
                    "text": "#000000",  # Black
                },
            },
            Theme.COLORBLIND_FRIENDLY.value: {
                "background": "white",
                "text": "black",
                "grid": "#CCCCCC",  # Light gray
                "array": {
                    "normal": "#E8E8E8",  # Very light gray
                    "comparing": "#F4D03F",  # Yellow (distinct)
                    "swapping": "#E74C3C",  # Red (distinct)
                    "sorted": "#27AE60",  # Green (distinct)
                    "current": "#F39C12",  # Orange (distinct)
                    "highlighted": "#9B59B6",  # Purple (distinct)
                    "edge": "#2C3E50",  # Dark blue-gray
                    "text": "#2C3E50",  # Dark blue-gray
                },
                "tree": {
                    "node": "#ECF0F1",  # Light gray-blue
                    "node_highlighted": "#F4D03F",  # Yellow
                    "node_current": "#F39C12",  # Orange
                    "edge": "#34495E",  # Dark gray-blue
                    "text": "#2C3E50",  # Dark blue-gray
                },
                "graph": {
                    "vertex": "#BDC3C7",  # Medium gray
                    "vertex_visited": "#27AE60",  # Green
                    "vertex_current": "#F39C12",  # Orange
                    "edge": "#7F8C8D",  # Medium gray-blue
                    "edge_highlighted": "#E74C3C",  # Red
                    "text": "#2C3E50",  # Dark blue-gray
                },
                "hash_table": {
                    "bucket": "#ECF0F1",  # Light gray-blue
                    "bucket_highlighted": "#F4D03F",  # Yellow
                    "item": "#BDC3C7",  # Medium gray
                    "item_highlighted": "#F39C12",  # Orange
                    "edge": "#34495E",  # Dark gray-blue
                    "text": "#2C3E50",  # Dark blue-gray
                },
            },
        }

    def get_theme(self) -> Theme:
        """Get current theme."""
        return self._theme

    def set_theme(self, theme: Theme) -> None:
        """
        Set the active theme.

        Args:
            theme: Theme to use
        """
        self._theme = theme

    def get_colors(self, data_structure_type: str) -> Dict[str, str]:
        """
        Get colors for a specific data structure type.

        Args:
            data_structure_type: Type of data structure ('array', 'tree', 'graph', 'hash_table')

        Returns:
            Dictionary of color names to color values
        """
        theme_colors = self._themes[self._theme.value]
        return theme_colors.get(data_structure_type, {})

    def get_color(self, data_structure_type: str, color_name: str, default: str = "gray") -> str:
        """
        Get a specific color for a data structure type.

        Args:
            data_structure_type: Type of data structure
            color_name: Name of the color (e.g., 'normal', 'comparing', 'sorted')
            default: Default color if not found

        Returns:
            Color value as string
        """
        colors = self.get_colors(data_structure_type)
        return colors.get(color_name, default)

    def get_background_color(self) -> str:
        """Get background color for current theme."""
        return self._themes[self._theme.value]["background"]

    def get_text_color(self) -> str:
        """Get text color for current theme."""
        return self._themes[self._theme.value]["text"]

    def get_grid_color(self) -> str:
        """Get grid color for current theme."""
        return self._themes[self._theme.value]["grid"]

    @classmethod
    def list_themes(cls) -> list[str]:
        """
        List all available theme names.

        Returns:
            List of theme names
        """
        return [theme.value for theme in Theme]

