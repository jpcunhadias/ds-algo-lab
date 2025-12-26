"""
Interactive controls for algorithm visualizations.
Provides play/pause/step controls and parameter modification.
"""

from typing import Any, Callable, Dict, List, Optional

import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Button, Slider

from ..utils.config import get_config
from .insights_panel import InsightsPanel
from .performance_panel import PerformancePanel
from .variable_tracker import VariableTracker


class InteractiveControls:
    """
    Interactive controls for navigating through algorithm visualizations.
    """

    def __init__(
        self,
        steps: List[Dict[str, Any]],
        visualizer,
        update_callback: Optional[Callable] = None,
        show_code_overlay: bool = False,
        show_variable_tracker: bool = True,
        show_performance_panel: bool = True,
        show_insights: bool = True,
        on_close_callback: Optional[Callable] = None,
    ):
        """
        Initialize interactive controls.

        Args:
            steps: List of algorithm steps
            visualizer: Visualizer instance
            update_callback: Optional callback for visualization updates
            show_code_overlay: Whether to show code overlay (default: False, disabled for now)
            show_variable_tracker: Whether to show variable tracker
            show_performance_panel: Whether to show performance panel
            show_insights: Whether to show insights panel
            on_close_callback: Optional callback called when window closes
        """
        self.steps = steps
        self.visualizer = visualizer
        self.update_callback = update_callback
        self.on_close_callback = on_close_callback
        self.current_step = 0
        self.playing = False
        self.animation_speed = 1.0  # Speed multiplier (higher = faster)
        self.fig = None
        self.ax = None
        self.animation = None
        self._animation_timer = None  # Keep timer reference

        # Load config
        config = get_config()
        self.show_code_overlay = config.get(
            "display.show_code_overlay", show_code_overlay
        )
        self.show_variable_tracker = config.get(
            "display.show_variable_tracker", show_variable_tracker
        )
        self.show_performance_panel = config.get(
            "display.show_performance_panel", show_performance_panel
        )
        self.show_insights = config.get("display.show_insights_panel", show_insights)

        # Initialize panels (code overlay disabled for now)
        self.code_overlay = None
        self.variable_tracker = VariableTracker()
        self.performance_panel = PerformancePanel()
        self.insights_panel = None

        # Initialize insights panel
        if self.show_insights and steps:
            first_step = steps[0]
            algorithm_name = first_step.get("algorithm", "")

            # For tree operations, use operation name
            if not algorithm_name and "operation" in first_step:
                operation = first_step.get("operation", "")
                ds = first_step.get("data_structure")
                if ds:
                    state = ds.get_state()
                    ds_type = state.get("type", "")
                    if "BST" in ds_type or "BinarySearchTree" in ds_type:
                        algorithm_name = f"BST {operation.title()}"
                    elif "Tree" in ds_type:
                        if (
                            "traversal" in operation.lower()
                            or "traverse" in operation.lower()
                        ):
                            algorithm_name = "Tree Traversal"
                        else:
                            algorithm_name = f"Tree {operation.title()}"
                    else:
                        algorithm_name = operation.title()

            if algorithm_name:
                self.insights_panel = InsightsPanel(algorithm_name)

    def show(self):
        """Display interactive visualization with controls."""
        # Create figure with grid layout for panels
        self.fig = plt.figure(figsize=(18, 10))

        # Calculate grid layout based on enabled panels
        num_panels = sum(
            [
                self.show_code_overlay,
                self.show_variable_tracker,
                self.show_performance_panel,
                self.show_insights,
            ]
        )

        if num_panels > 0:
            # Use GridSpec for complex layout
            gs = GridSpec(
                2,
                3,
                figure=self.fig,
                hspace=0.3,
                wspace=0.3,
                left=0.05,
                right=0.95,
                top=0.95,
                bottom=0.15,
            )

            # Main visualization area (larger - spans more columns since no code overlay)
            self.ax = self.fig.add_subplot(gs[0, :])

            # Bottom panels
            panel_idx = 0
            if self.show_variable_tracker:
                ax_vars = self.fig.add_subplot(gs[1, 0])
                self.variable_tracker.render(ax_vars, position="bottom")
                panel_idx += 1

            if self.show_performance_panel:
                ax_perf = self.fig.add_subplot(gs[1, 1])
                self.performance_panel.render(ax_perf)
                panel_idx += 1

            if self.show_insights and self.insights_panel:
                ax_insights = self.fig.add_subplot(gs[1, 2])
                self.insights_panel.render(ax_insights)
                panel_idx += 1
        else:
            # Simple layout without panels
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

        btn_prev = Button(ax_prev, "Previous")
        btn_play = Button(ax_play, "Play")
        btn_pause = Button(ax_pause, "Pause")
        btn_next = Button(ax_next, "Next")
        btn_reset = Button(ax_reset, "Reset")
        slider_speed = Slider(ax_speed, "Speed", 0.1, 2.0, valinit=self.animation_speed)

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

        # Connect close event callback
        self._close_callback_called = False
        if self.on_close_callback:
            self.fig.canvas.mpl_connect("close_event", self._on_close)

        plt.show()

    def _on_close(self, event):
        """Handle window close event."""
        # Prevent multiple calls to callback
        if self.on_close_callback and not self._close_callback_called:
            self._close_callback_called = True
            try:
                self.on_close_callback()
            except Exception as e:
                # Prevent callback errors from causing issues
                print(f"Error in close callback: {e}")

    def _update_display(self):
        """Update the visualization display."""
        if not self.steps or self.current_step >= len(self.steps):
            return

        self.ax.clear()
        step = self.steps[self.current_step]
        data_structure = step.get("data_structure")

        if data_structure and self.visualizer:
            # Pass our axes and figure to the visualizer so it draws on them
            self.visualizer.visualize(data_structure, step, ax=self.ax, fig=self.fig)

        # Update variable tracker
        if self.show_variable_tracker:
            variables = self.variable_tracker.extract_from_step(step)
            self.variable_tracker.update(variables)

        # Update performance panel
        if self.show_performance_panel:
            self.performance_panel.extract_from_step(step)

        # Add step info
        step_info = f"Step {self.current_step + 1}/{len(self.steps)}"
        if "description" in step:
            step_info += f": {step['description']}"
        self.ax.text(
            0.5,
            0.95,
            step_info,
            transform=self.ax.transAxes,
            ha="center",
            fontsize=12,
            fontweight="bold",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

        # Redraw panels (if using GridSpec layout)
        if hasattr(self, "metric_axes") or len(self.fig.axes) > 1:
            # Find panel axes and re-render
            panel_axes = [ax for ax in self.fig.axes if ax != self.ax]
            panel_idx = 0

            if self.show_variable_tracker and panel_idx < len(panel_axes):
                self.variable_tracker.render(panel_axes[panel_idx], position="bottom")
                panel_idx += 1

            if self.show_performance_panel and panel_idx < len(panel_axes):
                self.performance_panel.render(panel_axes[panel_idx])
                panel_idx += 1

            if (
                self.show_insights
                and self.insights_panel
                and panel_idx < len(panel_axes)
            ):
                self.insights_panel.render(panel_axes[panel_idx])

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
                if (
                    hasattr(self.animation, "event_source")
                    and self.animation.event_source
                ):
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
                    if (
                        self.animation
                        and hasattr(self.animation, "event_source")
                        and self.animation.event_source
                    ):
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
            cache_frame_data=False,
        )

        # CRITICAL: Store animation reference in multiple places to prevent garbage collection
        self.fig._animation = self.animation
        # Store timer reference to keep it alive (this is what makes speed slider work)
        try:
            if hasattr(self.animation, "event_source") and self.animation.event_source:
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
                "step_number": self.current_step + 1,
                "total_steps": len(self.steps),
                "step_data": self.steps[self.current_step],
            }
        return {}
