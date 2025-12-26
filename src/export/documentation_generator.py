"""
Documentation Generator
Generates visual documentation from algorithms and tutorials.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from ..visualization.algo_visualizer import AlgorithmVisualizer
from ..visualization.insights_panel import InsightsPanel
from ..tutorials.algorithm_explanations import AlgorithmExplanations
from ..playground.sorting_playground import SortingPlayground
from ..playground.searching_playground import SearchingPlayground


class DocumentationGenerator:
    """
    Generates visual documentation from algorithms.
    """

    def __init__(self):
        """Initialize documentation generator."""
        pass

    def generate_algorithm_reference(
        self,
        algorithm_name: str,
        input_data: List[Any],
        output_file: str,
        include_explanation: bool = True,
    ) -> str:
        """
        Generate a reference card for an algorithm.

        Args:
            algorithm_name: Name of the algorithm
            input_data: Sample input data
            output_file: Output PDF filename
            include_explanation: Whether to include algorithm explanation

        Returns:
            Path to generated PDF
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with PdfPages(output_file) as pdf:
            # Page 1: Algorithm overview and insights
            if include_explanation:
                fig = plt.figure(figsize=(11, 8.5))
                ax = fig.add_subplot(111)
                ax.axis("off")

                explanation = AlgorithmExplanations.get_explanation(algorithm_name)
                if explanation:
                    y_pos = 0.95
                    ax.text(0.5, y_pos, algorithm_name, ha="center", va="top",
                           fontsize=20, fontweight="bold", transform=ax.transAxes)

                    y_pos -= 0.1
                    ax.text(0.1, y_pos, "Overview:", fontsize=14, fontweight="bold",
                           transform=ax.transAxes)
                    y_pos -= 0.08
                    ax.text(0.1, y_pos, explanation.overview, fontsize=11,
                           transform=ax.transAxes, wrap=True)

                    y_pos -= 0.15
                    ax.text(0.1, y_pos, "How It Works:", fontsize=14, fontweight="bold",
                           transform=ax.transAxes)
                    y_pos -= 0.08
                    ax.text(0.1, y_pos, explanation.how_it_works, fontsize=11,
                           transform=ax.transAxes, wrap=True)

                    y_pos -= 0.15
                    ax.text(0.1, y_pos, f"Time Complexity: {explanation.complexity['time']}",
                           fontsize=12, fontweight="bold", transform=ax.transAxes)
                    y_pos -= 0.06
                    ax.text(0.1, y_pos, f"Space Complexity: {explanation.complexity['space']}",
                           fontsize=12, fontweight="bold", transform=ax.transAxes)

                pdf.savefig(fig, bbox_inches="tight")
                plt.close(fig)

            # Page 2+: Visualization steps
            pg = SortingPlayground() if "sort" in algorithm_name.lower() else SearchingPlayground()
            pg.set_input(input_data)

            if "search" in algorithm_name.lower():
                # For search algorithms, need target
                target = input_data[len(input_data) // 2] if input_data else None
                if target:
                    pg.set_target(target)

            steps = pg.run_algorithm(algorithm_name.lower().replace(" ", "_"))
            visualizer = AlgorithmVisualizer()

            # Create pages with multiple steps per page
            steps_per_page = 4
            for page_start in range(0, len(steps), steps_per_page):
                fig, axes = plt.subplots(2, 2, figsize=(11, 8.5))
                axes = axes.flatten()

                page_steps = steps[page_start : page_start + steps_per_page]
                for i, step in enumerate(page_steps):
                    if i < len(axes):
                        ax = axes[i]
                        data_structure = step.get("data_structure")
                        if data_structure:
                            visualizer.visualize(data_structure, step, ax=ax, fig=fig)
                            step_num = step.get("step_number", page_start + i + 1)
                            ax.set_title(f"Step {step_num}", fontsize=10, fontweight="bold")

                plt.tight_layout()
                pdf.savefig(fig, bbox_inches="tight")
                plt.close(fig)

        return output_file

    def generate_tutorial_pdf(
        self, tutorial_title: str, content: List[Dict[str, Any]], output_file: str
    ) -> str:
        """
        Generate a tutorial PDF.

        Args:
            tutorial_title: Title of the tutorial
            content: List of content dictionaries with 'title', 'text', 'steps' keys
            output_file: Output PDF filename

        Returns:
            Path to generated PDF
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with PdfPages(output_file) as pdf:
            # Title page
            fig = plt.figure(figsize=(11, 8.5))
            ax = fig.add_subplot(111)
            ax.axis("off")
            ax.text(0.5, 0.5, tutorial_title, ha="center", va="center",
                   fontsize=24, fontweight="bold", transform=ax.transAxes)
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

            # Content pages
            for item in content:
                fig = plt.figure(figsize=(11, 8.5))
                ax = fig.add_subplot(111)
                ax.axis("off")

                y_pos = 0.95
                ax.text(0.5, y_pos, item.get("title", ""), ha="center", va="top",
                       fontsize=18, fontweight="bold", transform=ax.transAxes)

                y_pos -= 0.1
                text = item.get("text", "")
                ax.text(0.1, y_pos, text, fontsize=11, transform=ax.transAxes,
                       wrap=True, verticalalignment="top")

                pdf.savefig(fig, bbox_inches="tight")
                plt.close(fig)

        return output_file

    def generate_comparison_report(
        self,
        algorithm_names: List[str],
        input_data: List[Any],
        output_file: str,
    ) -> str:
        """
        Generate a comparison report for multiple algorithms.

        Args:
            algorithm_names: List of algorithm names to compare
            input_data: Input data to test
            output_file: Output PDF filename

        Returns:
            Path to generated PDF
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with PdfPages(output_file) as pdf:
            # Summary page
            fig = plt.figure(figsize=(11, 8.5))
            ax = fig.add_subplot(111)
            ax.axis("off")

            y_pos = 0.95
            ax.text(0.5, y_pos, "Algorithm Comparison Report", ha="center", va="top",
                   fontsize=20, fontweight="bold", transform=ax.transAxes)

            y_pos -= 0.1
            for algo_name in algorithm_names:
                explanation = AlgorithmExplanations.get_explanation(algo_name)
                if explanation:
                    y_pos -= 0.08
                    ax.text(0.1, y_pos, f"{algo_name}:", fontsize=14, fontweight="bold",
                           transform=ax.transAxes)
                    y_pos -= 0.06
                    ax.text(0.15, y_pos, f"Time: {explanation.complexity['time']}, "
                           f"Space: {explanation.complexity['space']}", fontsize=11,
                           transform=ax.transAxes)
                    y_pos -= 0.05

            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

            # Individual algorithm pages
            for algo_name in algorithm_names:
                self.generate_algorithm_reference(
                    algo_name, input_data, f"/tmp/{algo_name}_ref.pdf", include_explanation=False
                )
                # Copy pages from temp file (simplified - in practice would merge PDFs)

        return output_file

