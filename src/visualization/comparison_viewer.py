"""
Side-by-side algorithm comparison viewer.
"""

from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider


class ComparisonViewer:
    """
    Compare multiple algorithms side-by-side with synchronized playback.
    """

    def __init__(self):
        """Initialize the comparison viewer."""
        self.algorithms = []
        self.steps_list = []
        self.current_step = 0
        self.playing = False
        self.animation_speed = 0.5

    def add_algorithm(self, algorithm, data_structure, name: str):
        """
        Add an algorithm to compare.

        Args:
            algorithm: Algorithm instance
            data_structure: Array to run algorithm on (will be copied)
            name: Display name for the algorithm
        """
        # Lazy import to avoid circular dependencies
        from ..data_structures.array import Array

        # Create a copy of the data structure
        arr_copy = Array(data_structure.to_list())

        # Execute algorithm
        steps = algorithm.execute(arr_copy, visualize=False)

        self.algorithms.append({
            'name': name,
            'algorithm': algorithm,
            'steps': steps,
            'data_structure': arr_copy,
        })

    def compare(self, algorithms_config: List[Dict[str, Any]], input_data: List[Any]):
        """
        Compare multiple algorithms on the same input.

        Args:
            algorithms_config: List of dicts with 'algorithm', 'name' keys
            input_data: Input data to test on
        """
        self.algorithms = []

        # Lazy import to avoid circular dependencies
        from ..data_structures.array import Array

        for config in algorithms_config:
            arr = Array(input_data.copy())
            algo = config['algorithm']
            name = config['name']

            steps = algo.execute(arr, visualize=False)

            self.algorithms.append({
                'name': name,
                'algorithm': algo,
                'steps': steps,
                'data_structure': arr,
            })

    def show(self):
        """Display side-by-side comparison."""
        if not self.algorithms:
            print("No algorithms to compare. Add algorithms first.")
            return

        num_algorithms = len(self.algorithms)
        fig, axes = plt.subplots(1, num_algorithms, figsize=(6 * num_algorithms, 6))

        if num_algorithms == 1:
            axes = [axes]

        plt.subplots_adjust(bottom=0.2)

        # Create control buttons
        ax_prev = plt.axes([0.1, 0.05, 0.1, 0.04])
        ax_play = plt.axes([0.21, 0.05, 0.1, 0.04])
        ax_pause = plt.axes([0.32, 0.05, 0.1, 0.04])
        ax_next = plt.axes([0.43, 0.05, 0.1, 0.04])
        ax_reset = plt.axes([0.54, 0.05, 0.1, 0.04])
        ax_speed = plt.axes([0.65, 0.05, 0.25, 0.03])

        btn_prev = Button(ax_prev, 'Previous')
        btn_play = Button(ax_play, 'Play')
        btn_pause = Button(ax_pause, 'Pause')
        btn_next = Button(ax_next, 'Next')
        btn_reset = Button(ax_reset, 'Reset')
        slider_speed = Slider(ax_speed, 'Speed', 0.1, 2.0, valinit=self.animation_speed)

        # Store references
        self.fig = fig
        self.axes = axes
        self.btn_prev = btn_prev
        self.btn_next = btn_next
        self.btn_play = btn_play
        self.btn_pause = btn_pause
        self.btn_reset = btn_reset
        self.slider_speed = slider_speed

        # Button callbacks
        btn_prev.on_clicked(self._on_previous)
        btn_play.on_clicked(self._on_play)
        btn_pause.on_clicked(self._on_pause)
        btn_next.on_clicked(self._on_next)
        btn_reset.on_clicked(self._on_reset)
        slider_speed.on_changed(self._on_speed_change)

        # Display first step
        self._update_display()

        plt.show()

    def _update_display(self):
        """Update all algorithm visualizations."""
        max_steps = max(len(algo['steps']) for algo in self.algorithms)

        for i, algo_info in enumerate(self.algorithms):
            ax = self.axes[i]
            ax.clear()

            steps = algo_info['steps']
            step_index = min(self.current_step, len(steps) - 1)

            if steps:
                step = steps[step_index]
                data_structure = step.get('data_structure', algo_info['data_structure'])

                # Visualize this algorithm's step
                self._visualize_step(ax, data_structure, step, algo_info['name'])

    def _visualize_step(self, ax, data_structure, step: Dict[str, Any], name: str):
        """Visualize a single step for one algorithm."""
        import matplotlib.patches as patches

        state = data_structure.get_state()
        data = state.get('data', [])

        ax.set_xlim(-1, max(len(data), 10))
        ax.set_ylim(-0.5, 2.5)
        ax.set_aspect('equal')
        ax.axis('off')

        # Get step-specific information
        comparing = step.get('comparing', [])
        swapping = step.get('swapping', [])
        sorted_indices = step.get('sorted', [])
        current_indices = step.get('current', [])

        for j, value in enumerate(data):
            # Determine color
            if j in swapping:
                color = 'red'
            elif j in comparing:
                color = 'yellow'
            elif j in sorted_indices:
                color = 'green'
            elif j in current_indices:
                color = 'orange'
            else:
                color = 'lightblue'

            # Draw rectangle
            rect = patches.Rectangle(
                (j - 0.4, 0.5), 0.8, 1,
                linewidth=2, edgecolor='black', facecolor=color
            )
            ax.add_patch(rect)

            # Add value text
            ax.text(j, 1, str(value), ha='center', va='center',
                   fontsize=10, fontweight='bold')

        # Add title
        step_num = step.get('step_number', self.current_step + 1)
        title = f"{name}\nStep {step_num}"
        ax.set_title(title, fontsize=11, fontweight='bold')

    def _on_previous(self, event):
        """Handle previous button."""
        if self.current_step > 0:
            self.current_step -= 1
            self._update_display()

    def _on_next(self, event):
        """Handle next button."""
        max_steps = max(len(algo['steps']) for algo in self.algorithms)
        if self.current_step < max_steps - 1:
            self.current_step += 1
            self._update_display()

    def _on_play(self, event):
        """Handle play button."""
        self.playing = True
        self._animate()

    def _on_pause(self, event):
        """Handle pause button."""
        self.playing = False
        if hasattr(self, 'animation') and self.animation:
            self.animation.event_source.stop()

    def _on_reset(self, event):
        """Handle reset button."""
        self.playing = False
        self.current_step = 0
        if hasattr(self, 'animation') and self.animation:
            self.animation.event_source.stop()
        self._update_display()

    def _on_speed_change(self, val):
        """Handle speed change."""
        self.animation_speed = val
        if hasattr(self, 'animation') and self.animation:
            self.animation.event_source.interval = int(self.animation_speed * 1000)

    def _animate(self):
        """Animate through steps."""
        import matplotlib.animation as animation

        def animate_frame(frame):
            if not self.playing:
                return
            max_steps = max(len(algo['steps']) for algo in self.algorithms)
            if self.current_step < max_steps - 1:
                self.current_step += 1
                self._update_display()
            else:
                self.playing = False

        self.animation = animation.FuncAnimation(
            self.fig, animate_frame, interval=int(self.animation_speed * 1000),
            repeat=False
        )

    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for all algorithms.

        Returns:
            Dictionary with metrics for each algorithm
        """
        metrics = {}
        for algo_info in self.algorithms:
            name = algo_info['name']
            steps = algo_info['steps']

            # Count operations
            comparisons = sum(1 for s in steps if 'comparing' in s and s['comparing'])
            swaps = sum(1 for s in steps if 'swapping' in s and s['swapping'])

            metrics[name] = {
                'total_steps': len(steps),
                'comparisons': comparisons,
                'swaps': swaps,
            }

        return metrics

