"""
Sharing and saving capabilities for visualizations and playground states.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List


class VisualizationSharing:
    """
    Save and share visualizations and playground configurations.
    """

    def __init__(self, storage_dir: str = ".saved_visualizations"):
        """
        Initialize sharing system.

        Args:
            storage_dir: Directory to store saved visualizations
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_visualization(
        self,
        steps: List[Dict[str, Any]],
        metadata: Dict[str, Any],
        filename: Optional[str] = None,
    ) -> str:
        """
        Save visualization with metadata.

        Args:
            steps: Algorithm steps
            metadata: Metadata (title, algorithm name, etc.)
            filename: Optional filename (auto-generated if None)

        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            algo_name = metadata.get('algorithm_name', 'algorithm')
            filename = f"{algo_name}_{timestamp}.json"

        filepath = self.storage_dir / filename

        data = {
            'metadata': {
                **metadata,
                'saved_at': datetime.now().isoformat(),
            },
            'steps': self._simplify_steps(steps),
        }

        filepath.write_text(json.dumps(data, indent=2), encoding='utf-8')
        return str(filepath)

    def save_playground_state(
        self,
        playground_type: str,
        input_data: List[Any],
        algorithm_name: str,
        parameters: Dict[str, Any],
        filename: Optional[str] = None,
    ) -> str:
        """
        Save playground state for later reload.

        Args:
            playground_type: Type of playground ('sorting', 'searching', etc.)
            input_data: Input data
            algorithm_name: Algorithm name
            parameters: Algorithm parameters
            filename: Optional filename

        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{playground_type}_{algorithm_name}_{timestamp}.json"

        filepath = self.storage_dir / filename

        data = {
            'playground_type': playground_type,
            'input_data': input_data,
            'algorithm_name': algorithm_name,
            'parameters': parameters,
            'saved_at': datetime.now().isoformat(),
        }

        filepath.write_text(json.dumps(data, indent=2), encoding='utf-8')
        return str(filepath)

    def load_playground_state(self, filename: str) -> Dict[str, Any]:
        """
        Load a saved playground state.

        Args:
            filename: Filename to load

        Returns:
            Dictionary with playground state
        """
        filepath = self.storage_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"State file not found: {filename}")

        data = json.loads(filepath.read_text(encoding='utf-8'))
        return data

    def list_saved_visualizations(self) -> List[Dict[str, Any]]:
        """
        List all saved visualizations.

        Returns:
            List of visualization metadata
        """
        visualizations = []
        for filepath in self.storage_dir.glob("*.json"):
            try:
                data = json.loads(filepath.read_text(encoding='utf-8'))
                if 'metadata' in data:
                    visualizations.append({
                        'filename': filepath.name,
                        'metadata': data['metadata'],
                    })
            except Exception:
                continue
        return visualizations

    def add_note(self, filename: str, note: str) -> None:
        """
        Add a note to a saved visualization.

        Args:
            filename: Visualization filename
            note: Note text
        """
        filepath = self.storage_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Visualization not found: {filename}")

        data = json.loads(filepath.read_text(encoding='utf-8'))
        if 'notes' not in data['metadata']:
            data['metadata']['notes'] = []
        data['metadata']['notes'].append({
            'text': note,
            'created_at': datetime.now().isoformat(),
        })

        filepath.write_text(json.dumps(data, indent=2), encoding='utf-8')

    def _simplify_steps(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Simplify steps for JSON serialization."""
        simplified = []
        for step in steps:
            data_structure = step.get('data_structure')
            if data_structure:
                state = data_structure.get_state()
                simplified.append({
                    'step_number': step.get('step_number', 0),
                    'description': step.get('description', ''),
                    'data': state.get('data', []),
                    'comparing': step.get('comparing', []),
                    'swapping': step.get('swapping', []),
                    'sorted': step.get('sorted', []),
                    'current': step.get('current', []),
                })
        return simplified

