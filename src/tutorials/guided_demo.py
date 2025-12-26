"""
Guided Demonstrations
Pre-configured educational demonstrations with explanations.
"""

from typing import List, Dict, Any, Optional
from .visual_tutorial import VisualTutorial
from .algorithm_explanations import AlgorithmExplanations
from ..playground.sorting_playground import SortingPlayground
from ..playground.searching_playground import SearchingPlayground


class GuidedDemo:
    """
    Pre-configured demonstration with educational annotations.
    """

    def __init__(self, title: str, description: str):
        """
        Initialize guided demo.

        Args:
            title: Demo title
            description: Demo description
        """
        self.title = title
        self.description = description
        self.steps: List[Dict[str, Any]] = []

    def add_step(
        self,
        step_title: str,
        explanation: str,
        action: Optional[callable] = None,
        highlight_concepts: Optional[List[str]] = None,
    ) -> None:
        """
        Add a demonstration step.

        Args:
            step_title: Title of the step
            explanation: Explanation text
            action: Optional action to perform
            highlight_concepts: List of concepts to highlight
        """
        self.steps.append(
            {
                "title": step_title,
                "explanation": explanation,
                "action": action,
                "highlight_concepts": highlight_concepts or [],
            }
        )

    def run(self) -> None:
        """Run the guided demonstration."""
        print(f"\n{'='*70}")
        print(f"Guided Demo: {self.title}")
        print(f"{'='*70}")
        print(f"\n{self.description}\n")

        for i, step in enumerate(self.steps):
            print(f"\nStep {i+1}/{len(self.steps)}: {step['title']}")
            print("-" * 70)
            print(step["explanation"])

            if step["highlight_concepts"]:
                print("\nKey Concepts:")
                for concept in step["highlight_concepts"]:
                    print(f"  • {concept}")

            if step["action"]:
                response = input("\nPress Enter to see visualization (or 'q' to quit): ")
                if response.lower() == "q":
                    break
                step["action"]()

            if i < len(self.steps) - 1:
                input("\nPress Enter to continue...")

        print(f"\n{'='*70}")
        print("Demo completed!")
        print(f"{'='*70}\n")


class GuidedDemoLibrary:
    """Library of pre-configured guided demonstrations."""

    @staticmethod
    def bubble_sort_demo() -> GuidedDemo:
        """Create bubble sort guided demonstration."""
        demo = GuidedDemo(
            title="Bubble Sort Explained",
            description="Learn how bubble sort works step by step with visual examples.",
        )

        explanation = AlgorithmExplanations.get_explanation("Bubble Sort")

        demo.add_step(
            "Introduction to Bubble Sort",
            explanation.overview if explanation else "Bubble sort is a simple sorting algorithm.",
            highlight_concepts=["Adjacent comparison", "Repeated passes"],
        )

        demo.add_step(
            "How It Works",
            explanation.how_it_works if explanation else "The algorithm compares adjacent elements.",
            action=lambda: _run_sorting_demo("bubble_sort", [64, 34, 25, 12, 22, 11, 90]),
            highlight_concepts=["Swapping", "Early termination"],
        )

        demo.add_step(
            "Key Concepts",
            "Understanding the key concepts helps you master the algorithm.",
            highlight_concepts=explanation.key_concepts if explanation else [],
        )

        return demo

    @staticmethod
    def binary_search_demo() -> GuidedDemo:
        """Create binary search guided demonstration."""
        demo = GuidedDemo(
            title="Binary Search Explained",
            description="Learn how binary search efficiently finds elements in sorted arrays.",
        )

        explanation = AlgorithmExplanations.get_explanation("Binary Search")

        demo.add_step(
            "Introduction to Binary Search",
            explanation.overview if explanation else "Binary search finds elements in sorted arrays.",
            highlight_concepts=["Requires sorted array", "Divide and conquer"],
        )

        demo.add_step(
            "How It Works",
            explanation.how_it_works if explanation else "The algorithm divides the search space in half.",
            action=lambda: _run_searching_demo("binary_search", [10, 20, 30, 40, 50, 60, 70, 80, 90], 50),
            highlight_concepts=["Eliminating half the search space"],
        )

        demo.add_step(
            "Complexity Analysis",
            f"Time Complexity: {explanation.complexity['time']}, Space: {explanation.complexity['space']}"
            if explanation
            else "O(log n) time complexity",
            highlight_concepts=["Logarithmic time", "Constant space"],
        )

        return demo

    @staticmethod
    def sorting_comparison_demo() -> GuidedDemo:
        """Create sorting algorithms comparison demonstration."""
        demo = GuidedDemo(
            title="Sorting Algorithms Comparison",
            description="Compare different sorting algorithms to understand their trade-offs.",
        )

        demo.add_step(
            "Why Compare Algorithms?",
            "Different algorithms have different strengths. Understanding trade-offs helps you choose the right one.",
            highlight_concepts=["Time complexity", "Space complexity", "Stability"],
        )

        demo.add_step(
            "Bubble Sort vs Insertion Sort",
            "Both are O(n²), but insertion sort is more efficient for nearly sorted data.",
            action=lambda: _compare_sorting(["bubble_sort", "insertion_sort"], [64, 34, 25, 12, 22, 11, 90]),
            highlight_concepts=["Adaptive algorithms", "Best case performance"],
        )

        demo.add_step(
            "Divide and Conquer Algorithms",
            "Merge sort and quick sort use divide and conquer for better performance.",
            action=lambda: _compare_sorting(["merge_sort", "quick_sort"], [64, 34, 25, 12, 22, 11, 90]),
            highlight_concepts=["Divide and conquer", "O(n log n) complexity"],
        )

        return demo

    @staticmethod
    def list_demos() -> List[str]:
        """
        List available demonstrations.

        Returns:
            List of demo names
        """
        return [
            "bubble_sort_demo",
            "binary_search_demo",
            "sorting_comparison_demo",
        ]

    @staticmethod
    def get_demo(demo_name: str) -> Optional[GuidedDemo]:
        """
        Get a demonstration by name.

        Args:
            demo_name: Name of the demonstration

        Returns:
            GuidedDemo instance or None
        """
        demos = {
            "bubble_sort_demo": GuidedDemoLibrary.bubble_sort_demo,
            "binary_search_demo": GuidedDemoLibrary.binary_search_demo,
            "sorting_comparison_demo": GuidedDemoLibrary.sorting_comparison_demo,
        }

        demo_func = demos.get(demo_name)
        return demo_func() if demo_func else None


def _run_sorting_demo(algorithm_name: str, input_data: List[int]) -> None:
    """Helper function to run sorting demo."""
    pg = SortingPlayground()
    pg.set_input(input_data)
    steps = pg.run_algorithm(algorithm_name)
    pg.visualize(steps, interactive=True)


def _run_searching_demo(algorithm_name: str, input_data: List[int], target: int) -> None:
    """Helper function to run searching demo."""
    pg = SearchingPlayground()
    pg.set_input(input_data)
    pg.set_target(target)
    steps = pg.run_algorithm(algorithm_name)
    pg.visualize(steps, interactive=True)


def _compare_sorting(algorithm_names: List[str], input_data: List[int]) -> None:
    """Helper function to compare sorting algorithms."""
    pg = SortingPlayground()
    pg.set_input(input_data)
    pg.compare_algorithms(algorithm_names)

