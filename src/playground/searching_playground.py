"""
Searching algorithm playground for interactive exploration.
"""

from typing import List, Dict, Any, Optional
from .base import Playground, InputGenerator


class SearchingPlayground(Playground):
    """
    Interactive playground for exploring searching algorithms.
    """

    def __init__(self):
        """Initialize searching playground."""
        super().__init__("Searching Algorithms Playground")
        # Lazy imports to avoid circular dependencies
        from ..algorithms.searching.linear_search import LinearSearch
        from ..algorithms.searching.binary_search import BinarySearch

        self.algorithms = {
            'linear_search': LinearSearch,
            'binary_search': BinarySearch,
        }
        self.input_data: Optional[List[Any]] = None
        self.target_value: Optional[Any] = None

    def set_input(self, data: List[Any]) -> None:
        """
        Set input array (must be sorted for binary search).

        Args:
            data: Input data list
        """
        self.input_data = list(data)

    def set_target(self, target: Any) -> None:
        """
        Set target value to search for.

        Args:
            target: Target value
        """
        self.target_value = target

    def run_algorithm(self, algorithm_name: str, target: Optional[Any] = None, **kwargs) -> List[Dict[str, Any]]:
        """
        Run a searching algorithm.

        Args:
            algorithm_name: Name of algorithm
            target: Target value (uses self.target_value if None)
            **kwargs: Additional parameters

        Returns:
            List of algorithm steps
        """
        if self.input_data is None:
            raise ValueError("Input data not set. Use set_input() first.")

        target_val = target if target is not None else self.target_value
        if target_val is None:
            raise ValueError("Target value not set. Use set_target() or pass target parameter.")

        if algorithm_name not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")

        # Lazy import to avoid circular dependencies
        from ..data_structures.array import Array

        arr = Array(self.input_data.copy())
        algorithm = self.algorithms[algorithm_name]()
        steps = algorithm.execute(arr, target_val, visualize=False)

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

    def compare_algorithms(self, algorithm_names: List[str], target: Optional[Any] = None) -> None:
        """
        Compare multiple searching algorithms.

        Args:
            algorithm_names: List of algorithm names to compare
            target: Target value (uses self.target_value if None)
        """
        if self.input_data is None:
            raise ValueError("Input data not set. Use set_input() first.")

        target_val = target if target is not None else self.target_value
        if target_val is None:
            raise ValueError("Target value not set.")

        print(f"\nComparing algorithms for target: {target_val}")
        print("=" * 60)

        for name in algorithm_names:
            if name not in self.algorithms:
                print(f"Warning: Unknown algorithm {name}, skipping")
                continue

            try:
                steps = self.run_algorithm(name, target_val)
                final_step = steps[-1] if steps else {}
                found_index = final_step.get('found_index', -1)

                print(f"\n{name.replace('_', ' ').title()}:")
                print(f"  Steps: {len(steps)}")
                if found_index != -1:
                    print(f"  Found at index: {found_index}")
                else:
                    print(f"  Not found")
            except Exception as e:
                print(f"  Error: {e}")

    def get_available_algorithms(self) -> List[str]:
        """
        Get list of available searching algorithms.

        Returns:
            List of algorithm names
        """
        return list(self.algorithms.keys())

    def demo(self, algorithm_name: str, input_size: int = 20,
             target: Optional[Any] = None) -> None:
        """
        Run a quick demonstration.

        Args:
            algorithm_name: Algorithm to demonstrate
            input_size: Size of input array
            target: Target value (random if None)
        """
        # Generate sorted input (required for binary search)
        from .base import InputGenerator
        input_data = InputGenerator.sorted_array(input_size, start=1, step=2)

        if target is None:
            import random
            # Pick a random value from the array
            target = random.choice(input_data)

        print(f"Input (sorted): {input_data}")
        print(f"Target: {target}")
        self.set_input(input_data)
        self.set_target(target)

        # Run algorithm
        steps = self.run_algorithm(algorithm_name)
        print(f"Algorithm: {algorithm_name}")
        print(f"Total steps: {len(steps)}")

        # Visualize
        self.visualize(steps, interactive=True)

