"""
Enhanced visualization exporter supporting multiple formats including animations.
"""

import os
from typing import List, Optional, Union
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ..visualization.base import BaseVisualizer


class VisualizationExporter:
    """
    Exports visualizations to various formats including animations.
    """

    def __init__(self):
        """Initialize the exporter."""
        self.supported_formats = ['png', 'pdf', 'svg', 'gif', 'html']

    def export(
        self,
        visualizer: BaseVisualizer,
        filename: str,
        format: Optional[str] = None,
    ) -> str:
        """
        Export a single visualization.

        Args:
            visualizer: Visualizer instance with a figure
            filename: Output filename (extension determines format if format not specified)
            format: Optional format override ('png', 'pdf', 'svg')

        Returns:
            Path to saved file
        """
        if format is None:
            format = self._get_format_from_filename(filename)

        if format not in self.supported_formats:
            raise ValueError(f"Unsupported format: {format}. Supported: {self.supported_formats}")

        # Ensure directory exists
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == 'png':
            return self._export_png(visualizer, filename)
        elif format == 'pdf':
            return self._export_pdf(visualizer, filename)
        elif format == 'svg':
            return self._export_svg(visualizer, filename)
        else:
            raise ValueError(f"Format {format} not yet implemented for single exports")

    def export_animation(
        self,
        steps: List[dict],
        visualizer: BaseVisualizer,
        filename: str,
        duration: float = 0.5,
        format: str = 'gif',
    ) -> str:
        """
        Export an animated sequence (GIF or HTML).

        Args:
            steps: List of step dictionaries for animation
            visualizer: Visualizer instance
            filename: Output filename
            duration: Duration per frame in seconds
            format: Export format ('gif' or 'html')

        Returns:
            Path to saved file
        """
        if format == 'gif':
            return self._export_gif(steps, visualizer, filename, duration)
        elif format == 'html':
            return self._export_html_animation(steps, visualizer, filename, duration)
        else:
            raise ValueError(f"Unsupported animation format: {format}")

    def _export_gif(
        self,
        steps: List[dict],
        visualizer: BaseVisualizer,
        filename: str,
        duration: float,
    ) -> str:
        """Export animation as GIF."""
        try:
            from PIL import Image
        except ImportError:
            raise ImportError("PIL/Pillow is required for GIF export. Install with: pip install pillow")

        # Ensure directory exists
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Create temporary directory for frames
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()

        try:
            # Generate frames
            frame_files = []
            for i, step in enumerate(steps):
                data_structure = step.get('data_structure')
                if data_structure:
                    visualizer.visualize(data_structure, step)
                    frame_file = os.path.join(temp_dir, f"frame_{i:04d}.png")
                    visualizer.save(frame_file)
                    frame_files.append(frame_file)
                    plt.close('all')

            # Create GIF from frames
            if frame_files:
                images = [Image.open(f) for f in frame_files]
                images[0].save(
                    filename,
                    save_all=True,
                    append_images=images[1:],
                    duration=int(duration * 1000),
                    loop=0,
                )

            return filename

        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            plt.close('all')

    def _export_html_animation(
        self,
        steps: List[dict],
        visualizer: BaseVisualizer,
        filename: str,
        duration: float,
    ) -> str:
        """Export interactive HTML animation."""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Algorithm Visualization</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .controls {{ margin: 20px 0; }}
        button {{ margin: 5px; padding: 10px 15px; font-size: 14px; }}
        #canvas {{ border: 1px solid #ccc; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>Algorithm Visualization</h1>
    <div class="controls">
        <button onclick="previousStep()">Previous</button>
        <button onclick="playAnimation()">Play</button>
        <button onclick="pauseAnimation()">Pause</button>
        <button onclick="nextStep()">Next</button>
        <button onclick="resetAnimation()">Reset</button>
        <span>Step: <span id="stepInfo">1/{len(steps)}</span></span>
    </div>
    <div id="canvas"></div>

    <script>
        const steps = {self._steps_to_json(steps)};
        let currentStep = 0;
        let playing = false;
        let animationInterval = null;
        const duration = {duration * 1000};

        function updateDisplay() {{
            const step = steps[currentStep];
            document.getElementById('stepInfo').textContent = `${{currentStep + 1}}/${{steps.length}}`;
            // Render step visualization here
            // This is a simplified version - full implementation would render SVG/Canvas
        }}

        function previousStep() {{
            if (currentStep > 0) {{
                currentStep--;
                updateDisplay();
            }}
        }}

        function nextStep() {{
            if (currentStep < steps.length - 1) {{
                currentStep++;
                updateDisplay();
            }}
        }}

        function playAnimation() {{
            if (!playing) {{
                playing = true;
                animationInterval = setInterval(() => {{
                    if (currentStep < steps.length - 1) {{
                        currentStep++;
                        updateDisplay();
                    }} else {{
                        pauseAnimation();
                    }}
                }}, duration);
            }}
        }}

        function pauseAnimation() {{
            playing = false;
            if (animationInterval) {{
                clearInterval(animationInterval);
                animationInterval = null;
            }}
        }}

        function resetAnimation() {{
            pauseAnimation();
            currentStep = 0;
            updateDisplay();
        }}

        updateDisplay();
    </script>
</body>
</html>"""

        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content)
        return filename

    def _steps_to_json(self, steps: List[dict]) -> str:
        """Convert steps to JSON string."""
        import json
        # Simplify steps for JSON serialization
        simplified = []
        for step in steps:
            data_structure = step.get('data_structure')
            if data_structure:
                state = data_structure.get_state()
                simplified.append({
                    'step_number': step.get('step_number', 0),
                    'description': step.get('description', ''),
                    'data': state.get('data', []),
                })
        return json.dumps(simplified)

    def export_pdf_pages(
        self,
        steps: List[dict],
        visualizer: BaseVisualizer,
        filename: str,
    ) -> str:
        """
        Export multiple steps as pages in a single PDF.

        Args:
            steps: List of step dictionaries
            visualizer: Visualizer instance
            filename: Output PDF filename

        Returns:
            Path to saved PDF file
        """
        try:
            from matplotlib.backends.backend_pdf import PdfPages
        except ImportError:
            raise ImportError("matplotlib is required for PDF export")

        # Ensure directory exists
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with PdfPages(filename) as pdf:
            for step in steps:
                data_structure = step.get('data_structure')
                if data_structure:
                    visualizer.visualize(data_structure, step)
                    if visualizer._figure:
                        pdf.savefig(visualizer._figure, bbox_inches='tight')
                        plt.close(visualizer._figure)

        return filename

    def _export_png(self, visualizer: BaseVisualizer, filename: str) -> str:
        """Export as PNG."""
        visualizer.save(filename)
        return filename

    def _export_pdf(self, visualizer: BaseVisualizer, filename: str) -> str:
        """Export as PDF."""
        if visualizer._figure:
            visualizer._figure.savefig(filename, format='pdf', bbox_inches='tight')
        else:
            plt.savefig(filename, format='pdf', bbox_inches='tight')
        return filename

    def _export_svg(self, visualizer: BaseVisualizer, filename: str) -> str:
        """Export as SVG."""
        if visualizer._figure:
            visualizer._figure.savefig(filename, format='svg', bbox_inches='tight')
        else:
            plt.savefig(filename, format='svg', bbox_inches='tight')
        return filename

    def _get_format_from_filename(self, filename: str) -> str:
        """Extract format from filename extension."""
        ext = Path(filename).suffix.lower().lstrip('.')
        if ext in self.supported_formats:
            return ext
        return 'png'  # Default

