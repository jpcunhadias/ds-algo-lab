"""
Animation Engine
Provides smooth transitions between visualization steps with interpolation.
"""

from typing import List, Dict, Any, Callable, Optional
import numpy as np


class AnimationCurve:
    """Animation curve types for smooth transitions."""

    @staticmethod
    def linear(t: float) -> float:
        """Linear interpolation."""
        return t

    @staticmethod
    def ease_in(t: float) -> float:
        """Ease-in curve (slow start, fast end)."""
        return t * t

    @staticmethod
    def ease_out(t: float) -> float:
        """Ease-out curve (fast start, slow end)."""
        return 1 - (1 - t) * (1 - t)

    @staticmethod
    def ease_in_out(t: float) -> float:
        """Ease-in-out curve (slow start and end, fast middle)."""
        return 0.5 * (2 * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2)

    @staticmethod
    def smooth_step(t: float) -> float:
        """Smooth step function."""
        return t * t * (3 - 2 * t)


class AnimationEngine:
    """
    Engine for creating smooth animations between visualization steps.
    Provides interpolation and transition effects.
    """

    def __init__(
        self,
        curve: Callable[[float], float] = AnimationCurve.ease_in_out,
        frames_per_step: int = 5,
    ):
        """
        Initialize animation engine.

        Args:
            curve: Animation curve function (default: ease_in_out)
            frames_per_step: Number of intermediate frames between steps
        """
        self.curve = curve
        self.frames_per_step = frames_per_step

    def interpolate_steps(
        self, steps: List[Dict[str, Any]], include_intermediate: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Create intermediate steps for smooth animation.

        Args:
            steps: List of step dictionaries
            include_intermediate: Whether to include intermediate frames

        Returns:
            List of steps with interpolated intermediate steps
        """
        if not include_intermediate or len(steps) <= 1:
            return steps

        interpolated = []
        for i in range(len(steps) - 1):
            current_step = steps[i]
            next_step = steps[i + 1]

            # Add current step
            interpolated.append(current_step)

            # Add intermediate steps
            for frame in range(1, self.frames_per_step):
                t = frame / self.frames_per_step
                eased_t = self.curve(t)
                intermediate = self._interpolate_step(current_step, next_step, eased_t)
                interpolated.append(intermediate)

        # Add final step
        interpolated.append(steps[-1])

        return interpolated

    def _interpolate_step(
        self, step1: Dict[str, Any], step2: Dict[str, Any], t: float
    ) -> Dict[str, Any]:
        """
        Interpolate between two steps.

        Args:
            step1: First step
            step2: Second step
            t: Interpolation parameter (0.0 to 1.0)

        Returns:
            Interpolated step dictionary
        """
        # Start with step1 as base
        interpolated = step1.copy()

        # Interpolate data structure state
        ds1 = step1.get("data_structure")
        ds2 = step2.get("data_structure")

        if ds1 and ds2:
            state1 = ds1.get_state()
            state2 = ds2.get_state()
            data1 = state1.get("data", [])
            data2 = state2.get("data", [])

            if len(data1) == len(data2):
                # Interpolate numeric values
                interpolated_data = []
                for v1, v2 in zip(data1, data2):
                    if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                        interpolated_data.append(v1 + (v2 - v1) * t)
                    else:
                        # Use step2 value if types don't match or t > 0.5
                        interpolated_data.append(v2 if t > 0.5 else v1)

                # Create new data structure with interpolated data
                from ..data_structures.array import Array

                interpolated_ds = Array(interpolated_data)
                interpolated["data_structure"] = interpolated_ds

        # Interpolate positions for visual elements
        # This is useful for smooth movement animations
        if "comparing" in step1 and "comparing" in step2:
            # Blend comparing states
            if t < 0.5:
                interpolated["comparing"] = step1.get("comparing", [])
            else:
                interpolated["comparing"] = step2.get("comparing", [])

        if "swapping" in step1 and "swapping" in step2:
            # Blend swapping states
            if t < 0.5:
                interpolated["swapping"] = step1.get("swapping", [])
            else:
                interpolated["swapping"] = step2.get("swapping", [])

        # Update step number
        step_num1 = step1.get("step_number", 0)
        step_num2 = step2.get("step_number", 0)
        interpolated["step_number"] = int(step_num1 + (step_num2 - step_num1) * t)

        # Blend descriptions
        desc1 = step1.get("description", "")
        desc2 = step2.get("description", "")
        if desc1 != desc2:
            interpolated["description"] = desc1 if t < 0.5 else desc2

        return interpolated

    def interpolate_color(self, color1: str, color2: str, t: float) -> str:
        """
        Interpolate between two colors.

        Args:
            color1: First color (hex or named)
            color2: Second color (hex or named)
            t: Interpolation parameter (0.0 to 1.0)

        Returns:
            Interpolated color as hex string
        """
        try:
            import matplotlib.colors as mcolors

            # Convert colors to RGB
            rgb1 = np.array(mcolors.to_rgb(color1))
            rgb2 = np.array(mcolors.to_rgb(color2))

            # Interpolate
            rgb_interp = rgb1 + (rgb2 - rgb1) * t

            # Convert back to hex
            return mcolors.to_hex(rgb_interp)
        except Exception:
            # Fallback: return color2 if t > 0.5, else color1
            return color2 if t > 0.5 else color1

    def set_curve(self, curve: Callable[[float], float]) -> None:
        """
        Set animation curve function.

        Args:
            curve: Animation curve function
        """
        self.curve = curve

    def set_frames_per_step(self, frames: int) -> None:
        """
        Set number of frames per step.

        Args:
            frames: Number of intermediate frames
        """
        self.frames_per_step = max(1, frames)

