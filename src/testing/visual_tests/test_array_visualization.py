"""
Visual test for Array data structure visualization.
"""

from pathlib import Path

from src.data_structures.array import Array
from src.visualization.ds_visualizer import DataStructureVisualizer


def test_array_visualization():
    """Test array visualization."""
    # Create output directory if it doesn't exist
    output_dir = Path(__file__).parent.parent.parent.parent / "test_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create array
    arr = Array([1, 2, 3, 4, 5])

    # Create visualizer
    visualizer = DataStructureVisualizer()
    arr.attach_visualizer(visualizer)

    # Visualize initial state
    visualizer.visualize(arr)
    output_file = output_dir / "array_initial.png"
    visualizer.save(str(output_file))
    print(f"Array visualization saved to {output_file}")

    # Perform operations
    arr.append(6)
    visualizer.visualize(arr)
    output_file = output_dir / "array_after_append.png"
    visualizer.save(str(output_file))
    print(f"Array after append saved to {output_file}")

    arr.insert(2, 10)
    visualizer.visualize(arr)
    output_file = output_dir / "array_after_insert.png"
    visualizer.save(str(output_file))
    print(f"Array after insert saved to {output_file}")


if __name__ == "__main__":
    test_array_visualization()
