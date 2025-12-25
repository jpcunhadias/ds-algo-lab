"""
Interactive controls for algorithm visualizations.
Provides play/pause/step controls and parameter modification.
"""

from typing import Callable, Optional, List, Dict, Any
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import matplotlib.animation as animation


class InteractiveControls:
    """
    Interactive controls for navigating through algorithm visualizations.
    """

    def __init__(self, steps: List[Dict[str, Any]], visualizer, update_callback: Optional[Callable] = None):
        """
        Initialize interactive controls.

        Args:
            steps: List of algorithm steps
            visualizer: Visualizer instance
            update_callback: Optional callback for visualization updates
        """
        self.steps = steps
        self.visualizer = visualizer
        self.update_callback = update_callback
        self.current_step = 0
        self.playing = False
        self.animation_speed = 1.0  # Speed multiplier (higher = faster)
        self.fig = None
        self.ax = None
        self.animation = None
        self._animation_timer = None  # Keep timer reference

    def show(self):
        """Display interactive visualization with controls."""
        self.fig, self.ax = plt.subplots(figsize=(14, 8))
        plt.subplots_adjust(bottom=0.2)

        # Create control buttons
        # Adjust positions to prevent overlap
        ax_prev = plt.axes([0.05, 0.05, 0.08, 0.04])
        ax_play = plt.axes([0.14, 0.05, 0.08, 0.04])
        ax_pause = plt.axes([0.23, 0.05, 0.08, 0.04])
        ax_next = plt.axes([0.32, 0.05, 0.08, 0.04])
        ax_reset = plt.axes([0.41, 0.05, 0.08, 0.04])
        # Speed slider positioned further right with more space (gap of 0.05)
        ax_speed = plt.axes([0.55, 0.05, 0.22, 0.03])

        btn_prev = Button(ax_prev, 'Previous')
        btn_play = Button(ax_play, 'Play')
        btn_pause = Button(ax_pause, 'Pause')
        btn_next = Button(ax_next, 'Next')
        btn_reset = Button(ax_reset, 'Reset')
        slider_speed = Slider(ax_speed, 'Speed', 0.1, 2.0, valinit=self.animation_speed)

        # Button callbacks
        btn_prev.on_clicked(self._on_previous)
        btn_play.on_clicked(self._on_play)
        btn_pause.on_clicked(self._on_pause)
        btn_next.on_clicked(self._on_next)
        btn_reset.on_clicked(self._on_reset)
        slider_speed.on_changed(self._on_speed_change)

        # Display first step
        self._update_display()

        # Store button references to prevent garbage collection
        self._btn_prev = btn_prev
        self._btn_play = btn_play
        self._btn_pause = btn_pause
        self._btn_next = btn_next
        self._btn_reset = btn_reset
        self._slider_speed = slider_speed

        plt.show()

    def _update_display(self):
        """Update the visualization display."""
        if not self.steps or self.current_step >= len(self.steps):
            return

        self.ax.clear()
        step = self.steps[self.current_step]
        data_structure = step.get('data_structure')

        if data_structure and self.visualizer:
            # Pass our axes and figure to the visualizer so it draws on them
            self.visualizer.visualize(data_structure, step, ax=self.ax, fig=self.fig)

        # Add step info
        step_info = f"Step {self.current_step + 1}/{len(self.steps)}"
        if 'description' in step:
            step_info += f": {step['description']}"
        self.ax.text(0.5, 0.95, step_info, transform=self.ax.transAxes,
                    ha='center', fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        self.fig.canvas.draw()

    def _on_previous(self, event):
        """Handle previous button click."""
        # Stop animation if playing
        if self.playing and self.animation and self.animation.event_source:
            self.playing = False
            self.animation.event_source.stop()

        if self.current_step > 0:
            self.current_step -= 1
            self._update_display()

    def _on_next(self, event):
        """Handle next button click."""
        # Stop animation if playing
        if self.playing and self.animation and self.animation.event_source:
            self.playing = False
            self.animation.event_source.stop()

        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._update_display()

    def _on_play(self, event):
        """Handle play button click."""
        if not self.playing:
            # Stop any existing animation first
            if self.animation and self.animation.event_source:
                self.animation.event_source.stop()
            self.playing = True
            self._animate()

    def _on_pause(self, event):
        """Handle pause button click."""
        self.playing = False
        if self.animation:
            self.animation.event_source.stop()

    def _on_reset(self, event):
        """Handle reset button click."""
        self.playing = False
        self.current_step = 0
        if self.animation and self.animation.event_source:
            self.animation.event_source.stop()
        self._update_display()

    def _on_speed_change(self, val):
        """Handle speed slider change."""
        self.animation_speed = val
        if self.animation and self.animation.event_source:
            # Higher speed value = faster = shorter interval
            # Convert speed (0.1-2.0) to interval in ms (5000ms to 500ms)
            base_interval = 1000  # Base interval in ms
            interval_ms = int(base_interval / self.animation_speed)
            self.animation.event_source.interval = interval_ms

    def _animate(self):
        """Animate through steps."""
        # Stop any existing animation first
        if self.animation:
            try:
                if hasattr(self.animation, 'event_source') and self.animation.event_source:
                    self.animation.event_source.stop()
            except:
                pass
            self.animation = None

        def animate_frame(frame):
            if not self.playing:
                return
            if self.current_step < len(self.steps) - 1:
                self.current_step += 1
                self._update_display()
            else:
                self.playing = False
                try:
                    if self.animation and hasattr(self.animation, 'event_source') and self.animation.event_source:
                        self.animation.event_source.stop()
                except:
                    pass

        # Calculate maximum frames needed
        max_frames = len(self.steps) - self.current_step
        if max_frames <= 0:
            return

        # Create animation
        # Higher speed value = faster = shorter interval
        # Convert speed (0.1-2.0) to interval in ms (5000ms to 500ms)
        base_interval = 1000  # Base interval in ms
        interval_ms = int(base_interval / self.animation_speed)

        self.animation = animation.FuncAnimation(
            self.fig,
            animate_frame,
            frames=max_frames,
            interval=interval_ms,
            repeat=False,
            cache_frame_data=False
        )

        # CRITICAL: Store animation reference in multiple places to prevent garbage collection
        self.fig._animation = self.animation
        # Store timer reference to keep it alive (this is what makes speed slider work)
        try:
            if hasattr(self.animation, 'event_source') and self.animation.event_source:
                self._animation_timer = self.animation.event_source
        except:
            pass

        # Force canvas to register the animation
        self.fig.canvas.draw_idle()

    def step_forward(self):
        """Programmatically step forward."""
        self._on_next(None)

    def step_backward(self):
        """Programmatically step backward."""
        self._on_previous(None)

    def go_to_step(self, step_index: int):
        """
        Jump to a specific step.

        Args:
            step_index: Step index (0-based)
        """
        if 0 <= step_index < len(self.steps):
            self.current_step = step_index
            self._update_display()

    def get_current_step_info(self) -> Dict[str, Any]:
        """
        Get information about current step.

        Returns:
            Dictionary with step information
        """
        if self.steps and 0 <= self.current_step < len(self.steps):
            return {
                'step_number': self.current_step + 1,
                'total_steps': len(self.steps),
                'step_data': self.steps[self.current_step],
            }
        return {}

