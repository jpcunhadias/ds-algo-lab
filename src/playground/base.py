"""
Base classes for interactive playgrounds.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from ..data_structures.array import Array


class InputGenerator:
    """
    Generate test data for algorithms.
    """

    @staticmethod
    def random(size: int, min_val: int = 1, max_val: int = 100) -> List[Any]:
        """
        Generate random array.

        Args:
            size: Size of array
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            List of random integers
        """
        import random
        return [random.randint(min_val, max_val) for _ in range(size)]

    @staticmethod
    def sorted_array(size: int, start: int = 1, step: int = 1) -> List[Any]:
        """
        Generate sorted array.

        Args:
            size: Size of array
            start: Starting value
            step: Step between values

        Returns:
            List of sorted integers
        """
        return list(range(start, start + size * step, step))

    @staticmethod
    def reversed_array(size: int, start: int = 1, step: int = 1) -> List[Any]:
        """
        Generate reverse sorted array.

        Args:
            size: Size of array
            start: Starting value
            step: Step between values

        Returns:
            List of reverse sorted integers
        """
        return list(range(start + size * step - step, start - step, -step))

    @staticmethod
    def nearly_sorted(size: int, swaps: int = 3) -> List[Any]:
        """
        Generate nearly sorted array.

        Args:
            size: Size of array
            swaps: Number of swaps to make

        Returns:
            Nearly sorted list
        """
        import random
        arr = list(range(1, size + 1))
        for _ in range(swaps):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    @staticmethod
    def duplicates(size: int, unique_values: int = 5) -> List[Any]:
        """
        Generate array with duplicates.

        Args:
            size: Size of array
            unique_values: Number of unique values

        Returns:
            List with duplicates
        """
        import random
        values = list(range(1, unique_values + 1))
        return [random.choice(values) for _ in range(size)]

    @staticmethod
    def pattern(pattern_name: str, size: int) -> List[Any]:
        """
        Generate array with specific pattern.

        Args:
            pattern_name: Name of pattern ('all_same', 'alternating', etc.)
            size: Size of array

        Returns:
            List with pattern
        """
        if pattern_name == 'all_same':
            return [5] * size
        elif pattern_name == 'alternating':
            return [1 if i % 2 == 0 else 2 for i in range(size)]
        elif pattern_name == 'increasing_then_decreasing':
            mid = size // 2
            return list(range(1, mid + 1)) + list(range(mid, 0, -1))
        else:
            return InputGenerator.random(size)


class Playground(ABC):
    """
    Base class for interactive algorithm playgrounds.
    """

    def __init__(self, title: str):
        """
        Initialize playground.

        Args:
            title: Playground title
        """
        self.title = title
        self.input_data: Optional[List[Any]] = None
        self.current_algorithm = None
        self.visualization_callback: Optional[Callable] = None

    @abstractmethod
    def set_input(self, data: List[Any]) -> None:
        """
        Set input data.

        Args:
            data: Input data list
        """
        pass

    @abstractmethod
    def run_algorithm(self, algorithm_name: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Run an algorithm on current input.

        Args:
            algorithm_name: Name of algorithm to run
            **kwargs: Algorithm-specific parameters

        Returns:
            List of algorithm steps
        """
        pass

    @abstractmethod
    def visualize(self, steps: List[Dict[str, Any]]) -> None:
        """
        Visualize algorithm steps.

        Args:
            steps: List of algorithm steps
        """
        pass

    def get_available_algorithms(self) -> List[str]:
        """
        Get list of available algorithms.

        Returns:
            List of algorithm names
        """
        return []

    def get_input_generators(self) -> Dict[str, Callable]:
        """
        Get available input generators.

        Returns:
            Dictionary mapping generator names to functions
        """
        return {
            'random': lambda size: InputGenerator.random(size),
            'sorted': lambda size: InputGenerator.sorted_array(size),
            'reversed': lambda size: InputGenerator.reversed_array(size),
            'nearly_sorted': lambda size: InputGenerator.nearly_sorted(size),
            'duplicates': lambda size: InputGenerator.duplicates(size),
        }

    def generate_input(self, generator_name: str, size: int, **kwargs) -> List[Any]:
        """
        Generate input using a generator.

        Args:
            generator_name: Name of generator
            size: Size of input
            **kwargs: Generator-specific parameters

        Returns:
            Generated input data
        """
        generators = self.get_input_generators()
        if generator_name in generators:
            return generators[generator_name](size, **kwargs)
        return InputGenerator.random(size)

