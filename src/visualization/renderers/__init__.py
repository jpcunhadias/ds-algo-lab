"""
Renderer abstraction layer for visualization backends.
"""

from .base_renderer import BaseRenderer
from .matplotlib_renderer import MatplotlibRenderer

__all__ = ["BaseRenderer", "MatplotlibRenderer"]

