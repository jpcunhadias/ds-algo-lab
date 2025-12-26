"""
Sorting algorithm playground for interactive exploration.
"""

from typing import List, Dict, Any, Optional
from .base import Playground, InputGenerator


class SortingPlayground(Playground):
    """
    Interactive playground for exploring sorting algorithms.
    """

    def __init__(self):
        """Initialize sorting playground."""
        super().__init__("Sorting Algorithms Playground")
        # Lazy imports to avoid circular dependencies
        from ..algorithms.sorting.bubble_sort import BubbleSort
        from ..algorithms.sorting.insertion_sort import InsertionSort
        from ..algorithms.sorting.selection_sort import SelectionSort
        from ..algorithms.sorting.merge_sort import MergeSort
        from ..algorithms.sorting.quick_sort import QuickSort
        from ..algorithms.sorting.heap_sort import HeapSort

        self.algorithms = {
            'bubble_sort': BubbleSort,
            'insertion_sort': InsertionSort,
            'selection_sort': SelectionSort,
            'merge_sort': MergeSort,
            'quick_sort': QuickSort,
            'heap_sort': HeapSort,
        }
        self.input_data: Optional[List[Any]] = None

    def set_input(self, data: List[Any]) -> None:
        """
        Set input array.

        Args:
            data: Input data list
        """
        self.input_data = list(data)

    def run_algorithm(self, algorithm_name: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Run a sorting algorithm.

        Args:
            algorithm_name: Name of algorithm
            **kwargs: Additional parameters

        Returns:
            List of algorithm steps
        """
        if self.input_data is None:
            raise ValueError("Input data not set. Use set_input() first.")

        if algorithm_name not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")

        # Lazy import to avoid circular dependencies
        from ..data_structures.array import Array

        arr = Array(self.input_data.copy())
        algorithm = self.algorithms[algorithm_name]()
        steps = algorithm.execute(arr, visualize=False)

        return steps

    def visualize(self, steps: List[Dict[str, Any]], interactive: bool = True) -> None:
        """
        Visualize algorithm steps.

        Args:
            steps: List of algorithm steps
            interactive: Whether to use interactive controls
        """
        if not steps:
            print("No steps to visualize")
            return

        # Lazy imports to avoid circular dependencies
        from ..visualization.algo_visualizer import AlgorithmVisualizer

        visualizer = AlgorithmVisualizer()

        if interactive:
            # Use interactive controls
            from ..visualization.interactive_controls import InteractiveControls
            controls = InteractiveControls(steps, visualizer)
            controls.show()
        else:
            # Simple animation
            visualizer.animate(steps)

    def compare_algorithms(self, algorithm_names: List[str]) -> None:
        """
        Compare multiple sorting algorithms side-by-side.

        Args:
            algorithm_names: List of algorithm names to compare
        """
        if self.input_data is None:
            raise ValueError("Input data not set. Use set_input() first.")

        # Lazy imports to avoid circular dependencies
        from ..visualization.comparison_viewer import ComparisonViewer
        from ..data_structures.array import Array

        viewer = ComparisonViewer()
        arr = Array(self.input_data.copy())

        for name in algorithm_names:
            if name not in self.algorithms:
                print(f"Warning: Unknown algorithm {name}, skipping")
                continue

            algo = self.algorithms[name]()
            viewer.add_algorithm(algo, arr, name.replace('_', ' ').title())

        viewer.show()

        # Print performance metrics
        metrics = viewer.get_performance_metrics()
        print("\nPerformance Metrics:")
        print("-" * 50)
        for algo_name, metric in metrics.items():
            print(f"{algo_name}:")
            print(f"  Total Steps: {metric['total_steps']}")
            print(f"  Comparisons: {metric['comparisons']}")
            print(f"  Swaps: {metric['swaps']}")
            print()

    def get_available_algorithms(self) -> List[str]:
        """
        Get list of available sorting algorithms.

        Returns:
            List of algorithm names
        """
        return list(self.algorithms.keys())

    def demo(self, algorithm_name: str, input_size: int = 10,
             input_type: str = 'random') -> None:
        """
        Run a quick demonstration.

        Args:
            algorithm_name: Algorithm to demonstrate
            input_size: Size of input array
            input_type: Type of input ('random', 'sorted', 'reversed', etc.)
        """
        # Generate input
        generators = self.get_input_generators()
        if input_type in generators:
            input_data = generators[input_type](input_size)
        else:
            input_data = InputGenerator.random(input_size)

        print(f"Input ({input_type}): {input_data}")
        self.set_input(input_data)

        # Run algorithm
        steps = self.run_algorithm(algorithm_name)
        print(f"Algorithm: {algorithm_name}")
        print(f"Total steps: {len(steps)}")

        # Visualize
        self.visualize(steps, interactive=True)

