"""
Base classes for data structures, algorithms, and visualizers.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseDataStructure(ABC):
    """
    Base class for all data structures.
    Provides visualization hooks and state management.
    """

    def __init__(self):
        """Initialize the data structure."""
        self._visualizer = None
        self._operation_history = []

    def attach_visualizer(self, visualizer):
        """
        Attach a visualizer to this data structure.

        Args:
            visualizer: The visualizer instance to attach
        """
        self._visualizer = visualizer

    def _notify_visualizer(self, event: str, data: Dict[str, Any]):
        """
        Notify the visualizer of a state change.

        Args:
            event: The event type (e.g., 'insert', 'delete', 'update')
            data: Dictionary containing event data
        """
        if self._visualizer:
            self._visualizer.update(event, data)

        # Store operation in history
        self._operation_history.append({"event": event, "data": data})

    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the data structure for visualization.

        Returns:
            Dictionary containing the current state
        """
        return {
            "type": self.__class__.__name__,
            "size": len(self),
            "data": self._get_internal_state(),
        }

    @abstractmethod
    def _get_internal_state(self) -> Any:
        """
        Get the internal state representation.
        Must be implemented by subclasses.

        Returns:
            Internal state representation
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Return the size of the data structure."""
        pass

    def __repr__(self) -> str:
        """String representation of the data structure."""
        return f"{self.__class__.__name__}({self._get_internal_state()})"


class BaseAlgorithm(ABC):
    """
    Base class for all algorithms.
    Provides step tracking and visualization support.
    """

    def __init__(self):
        """Initialize the algorithm."""
        self._visualizer = None
        self._steps = []
        self._current_step = 0

    def attach_visualizer(self, visualizer):
        """
        Attach a visualizer to this algorithm.

        Args:
            visualizer: The visualizer instance to attach
        """
        self._visualizer = visualizer

    def execute(self, data_structure, visualize: bool = True) -> List[Dict[str, Any]]:
        """
        Execute the algorithm on a data structure.

        Args:
            data_structure: The data structure to operate on
            visualize: Whether to visualize during execution

        Returns:
            List of execution steps
        """
        self._steps = []
        self._current_step = 0

        # Run the algorithm and collect steps
        for step in self._run(data_structure):
            self._steps.append(step)
            if visualize and self._visualizer:
                self._visualize_step(step)

        return self._steps

    def _visualize_step(self, step: Dict[str, Any]):
        """
        Visualize a single step of execution.

        Args:
            step: Dictionary containing step information
        """
        if self._visualizer:
            self._visualizer.update("step", step)

    @abstractmethod
    def _run(self, data_structure):
        """
        Run the algorithm logic.
        Must be implemented by subclasses.
        Should yield step dictionaries for visualization.

        Args:
            data_structure: The data structure to operate on

        Yields:
            Dictionary containing step information
        """
        pass

    def get_steps(self) -> List[Dict[str, Any]]:
        """
        Get all execution steps.

        Returns:
            List of step dictionaries
        """
        return self._steps

    def get_step(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific execution step.

        Args:
            index: The step index

        Returns:
            Step dictionary or None if index is out of bounds
        """
        if 0 <= index < len(self._steps):
            return self._steps[index]
        return None


class BaseVisualizer(ABC):
    """
    Base class for all visualizers.
    Provides common visualization interface.
    """

    def __init__(self):
        """Initialize the visualizer."""
        self._figure = None
        self._axes = None

    @abstractmethod
    def visualize(self, data_structure, step: Optional[Dict[str, Any]] = None):
        """
        Visualize the current state of a data structure.

        Args:
            data_structure: The data structure to visualize
            step: Optional step information for algorithm visualization
        """
        pass

    @abstractmethod
    def animate(self, steps: List[Dict[str, Any]]):
        """
        Animate through a series of steps.

        Args:
            steps: List of step dictionaries to animate
        """
        pass

    def update(self, event: str, data: Dict[str, Any]):
        """
        Update the visualization based on an event.

        Args:
            event: The event type
            data: Event data
        """
        if event == "step":
            # For algorithm steps
            self.visualize(data.get("data_structure"), step=data)
        else:
            # For data structure events
            self.visualize(data.get("data_structure"))

    def interactive_mode(self):
        """
        Enter interactive mode for user manipulation.
        """
        raise NotImplementedError(
            "Interactive mode not implemented for this visualizer"
        )

    def show(self):
        """Display the visualization."""
        try:
            import matplotlib.pyplot as plt

            plt.show()
        except ImportError:
            print(
                "matplotlib is required for visualization. Install it with: pip install matplotlib"
            )

    def save(self, filename: str):
        """
        Save the visualization to a file.

        Args:
            filename: The filename to save to
        """
        try:
            import matplotlib.pyplot as plt

            if self._figure:
                self._figure.savefig(filename)
            else:
                plt.savefig(filename)
        except ImportError:
            print(
                "matplotlib is required for visualization. Install it with: pip install matplotlib"
            )
