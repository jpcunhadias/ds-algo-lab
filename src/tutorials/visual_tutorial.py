"""
Visual tutorial system focused on demonstrations.
"""

from typing import Any, Dict, List, Optional

from ..visualization.algo_visualizer import AlgorithmVisualizer
from ..visualization.interactive_controls import InteractiveControls
from .algorithm_explanations import AlgorithmExplanations
from .base import StepType, Tutorial, TutorialStep


class VisualTutorial(Tutorial):
    """
    Visual tutorial with interactive demonstrations.
    """

    def __init__(self, title: str, description: str):
        """
        Initialize visual tutorial.

        Args:
            title: Tutorial title
            description: Tutorial description
        """
        super().__init__(title, description, [])
        self.demonstrations: List[Dict[str, Any]] = []

    def add_demonstration(
        self,
        title: str,
        description: str,
        code_example: Optional[str] = None,
        algorithm_steps: Optional[List[Dict[str, Any]]] = None,
        interactive: bool = True,
    ) -> None:
        """
        Add a visual demonstration step.

        Args:
            title: Step title
            description: Step description
            code_example: Optional code example
            algorithm_steps: Optional algorithm steps to visualize
            interactive: Whether demonstration is interactive
        """
        step = TutorialStep(
            step_type=StepType.VISUALIZATION,
            title=title,
            content=description,
            code=code_example,
        )

        self.add_step(step)

        # Store demonstration data
        self.demonstrations.append(
            {
                "title": title,
                "description": description,
                "code_example": code_example,
                "algorithm_steps": algorithm_steps,
                "interactive": interactive,
            }
        )

    def show_demonstration(self, step_index: int) -> None:
        """
        Show a specific demonstration.

        Args:
            step_index: Index of demonstration step
        """
        if step_index < 0 or step_index >= len(self.demonstrations):
            print(f"Invalid demonstration index: {step_index}")
            return

        demo = self.demonstrations[step_index]
        print(f"\n{'=' * 60}")
        print(f"Demonstration: {demo['title']}")
        print(f"{'=' * 60}")
        print(f"\n{demo['description']}")

        # Show algorithm explanation if available
        # Try to extract algorithm name from steps
        algorithm_name = demo.get("algorithm_name", "")
        if not algorithm_name and demo.get("algorithm_steps"):
            algorithm_name = (
                demo["algorithm_steps"][0].get("algorithm", "")
                if demo["algorithm_steps"]
                else ""
            )

        if algorithm_name:
            explanation = AlgorithmExplanations.get_explanation(algorithm_name)
            if explanation:
                print("\nAlgorithm Overview:")
                print(f"  {explanation.overview}")
                print("\nKey Concepts:")
                for concept in explanation.key_concepts[:3]:  # Show first 3
                    print(f"  • {concept}")

        if demo["code_example"]:
            print("\nCode Example:")
            print(demo["code_example"])

        if demo["algorithm_steps"]:
            print("\nVisualizing algorithm steps...")
            visualizer = AlgorithmVisualizer()

            if demo["interactive"]:
                # Use enhanced interactive controls with code overlay and variable tracker
                controls = InteractiveControls(
                    demo["algorithm_steps"],
                    visualizer,
                    show_code_overlay=True,
                    show_variable_tracker=True,
                    show_performance_panel=True,
                    show_insights=True,
                )
                controls.show()
            else:
                visualizer.animate(demo["algorithm_steps"])

    def run_tutorial(self) -> None:
        """Run the complete tutorial interactively."""
        print(f"\n{'=' * 60}")
        print(f"Tutorial: {self.title}")
        print(f"{'=' * 60}")
        print(f"\n{self.description}\n")

        for i, step in enumerate(self.steps):
            print(f"\nStep {i + 1}/{len(self.steps)}: {step.title}")
            print("-" * 60)
            print(step.content)

            if step.code:
                print("\nCode:")
                print(step.code)

            # Check if this step has a demonstration
            if i < len(self.demonstrations):
                demo = self.demonstrations[i]
                if demo["algorithm_steps"]:
                    response = input("\nShow visualization? (y/n): ")
                    if response.lower() == "y":
                        self.show_demonstration(i)

            if i < len(self.steps) - 1:
                input("\nPress Enter to continue to next step...")

        print(f"\n{'=' * 60}")
        print("Tutorial completed!")
        print(f"{'=' * 60}\n")
