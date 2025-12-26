"""
Base classes for tutorial system.
"""

from typing import List, Optional
from enum import Enum


class StepType(Enum):
    """Types of tutorial steps."""
    TEXT = "text"
    CODE = "code"
    VISUALIZATION = "visualization"
    EXERCISE = "exercise"


class TutorialStep:
    """Represents a single step in a tutorial."""

    def __init__(
        self,
        step_type: StepType,
        title: str,
        content: str,
        code: Optional[str] = None,
    ):
        """
        Initialize tutorial step.

        Args:
            step_type: Type of step
            title: Step title
            content: Step content/description
            code: Optional code example
        """
        self.step_type = step_type
        self.title = title
        self.content = content
        self.code = code


class Tutorial:
    """Base class for tutorials."""

    def __init__(self, title: str, description: str, steps: List[TutorialStep]):
        """
        Initialize tutorial.

        Args:
            title: Tutorial title
            description: Tutorial description
            steps: List of tutorial steps
        """
        self.title = title
        self.description = description
        self.steps = steps

    def add_step(self, step: TutorialStep) -> None:
        """
        Add a step to the tutorial.

        Args:
            step: Tutorial step to add
        """
        self.steps.append(step)

    def run(self) -> None:
        """Run the tutorial."""
        raise NotImplementedError("Subclasses must implement run()")

