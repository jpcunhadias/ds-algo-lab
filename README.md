# DSA Learning Playground

A Python-based interactive visual learning platform for exploring data structures and algorithms through demonstrations, visualizations, and experimentation. Focus on **visual understanding** and **interactive exploration** rather than problem-solving exercises.

## Features

- **Interactive Visualizations**: Step-by-step algorithm visualizations with play/pause/step controls
- **Algorithm Playgrounds**: Interactive environments for exploring sorting and searching algorithms
- **Side-by-Side Comparisons**: Compare multiple algorithms simultaneously with synchronized playback
- **Visual Demonstrations**: Guided visual tutorials showing how algorithms work
- **Implementation Testing**: Test your own algorithm implementations with visual feedback
- **Export Capabilities**: Export visualizations in multiple formats (PNG, PDF, SVG, GIF, HTML)
- **Input Builders**: Generate and modify test data visually
- **CLI Interface**: Easy command-line access to all features

## Project Structure

```
ds-algo-lab/
├── src/
│   ├── data_structures/     # Core DS implementations
│   ├── algorithms/          # Algorithm implementations
│   ├── visualization/       # Visualization engine with interactive controls
│   ├── playground/          # Interactive playgrounds for exploration
│   ├── testing/             # Testing framework for user implementations
│   ├── templates/            # Algorithm code templates
│   ├── tutorials/            # Visual tutorial system
│   ├── export/               # Export system (visualizations, sharing)
│   ├── cli/                  # Command-line interface
│   └── utils/                # Utilities
├── examples/                 # Example usage scripts
├── tests/                   # Test files
└── requirements.txt         # Python dependencies
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-Line Interface

Launch interactive playgrounds:

```bash
# Sorting playground
dsa-lab playground sorting

# Searching playground
dsa-lab playground searching

# Run a demonstration
dsa-lab demo bubble-sort

# Compare algorithms side-by-side
dsa-lab compare bubble-sort insertion-sort

# Test your implementation
dsa-lab test my_algorithm.py --function bubble_sort

# Get code template
dsa-lab template bubble_sort

# List all algorithms
dsa-lab list-algorithms
```

### Python API

#### Interactive Playgrounds

```python
from src.playground.sorting_playground import SortingPlayground

# Create playground
pg = SortingPlayground()

# Set input data
pg.set_input([64, 34, 25, 12, 22, 11, 90])

# Run algorithm with interactive visualization
steps = pg.run_algorithm('bubble_sort')
pg.visualize(steps, interactive=True)

# Compare multiple algorithms
pg.compare_algorithms(['bubble_sort', 'insertion_sort', 'selection_sort'])
```

#### Interactive Controls

```python
from src.data_structures.array import Array
from src.algorithms.sorting.bubble_sort import BubbleSort
from src.visualization.interactive_controls import InteractiveControls

# Run algorithm
arr = Array([64, 34, 25, 12, 22, 11, 90])
sorter = BubbleSort()
steps = sorter.execute(arr, visualize=False)

# Show with interactive controls
controls = InteractiveControls(steps, visualizer)
controls.show()  # Use play/pause/step controls
```

#### Algorithm Comparison

```python
from src.visualization.comparison_viewer import ComparisonViewer
from src.data_structures.array import Array
from src.algorithms.sorting.bubble_sort import BubbleSort
from src.algorithms.sorting.insertion_sort import InsertionSort

viewer = ComparisonViewer()
arr = Array([64, 34, 25, 12, 22, 11, 90])

viewer.add_algorithm(BubbleSort(), arr, "Bubble Sort")
viewer.add_algorithm(InsertionSort(), arr, "Insertion Sort")
viewer.show()  # Side-by-side comparison
```

#### Input Builder

```python
from src.playground.input_builder import InputBuilder

builder = InputBuilder()
builder.from_string("5, 2, 8, 1, 9")
arr = builder.to_array()
print(arr.to_list())  # [5, 2, 8, 1, 9]
```

#### Testing Implementations

```python
from src.testing.implementation_tester import ImplementationTester

tester = ImplementationTester()

code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
"""

result = tester.test_sorting_implementation(
    code, 'bubble_sort', [64, 34, 25, 12, 22, 11, 90], visualize=True
)

if result['success'] and result['correct']:
    print("✓ Implementation is correct!")
```

## Running Tests

```bash
pytest tests/
```

## Data Structures

- Array
- Linked List
- Stack
- Queue
- Binary Tree
- Binary Search Tree (BST)
- AVL Tree (Self-Balancing BST)
- Graph (with BFS and DFS)
- Hash Table (Hash Map)

## Algorithms

### Sorting
- Bubble Sort
- Insertion Sort
- Selection Sort
- Merge Sort
- Quick Sort
- Heap Sort

### Searching
- Linear Search
- Binary Search
- Ternary Search
- Exponential Search

## Interactive Features

### Visualization Controls
- **Play/Pause**: Control animation playback
- **Step Forward/Backward**: Navigate through algorithm steps manually
- **Speed Control**: Adjust animation speed
- **Reset**: Start over from the beginning

### Playgrounds
- **Sorting Playground**: Explore sorting algorithms with different input types
- **Searching Playground**: Visualize search algorithms on sorted arrays
- **Input Generators**: Random, sorted, reversed, nearly sorted, duplicates, patterns

### Comparison Tools
- **Side-by-Side View**: Compare multiple algorithms simultaneously
- **Performance Metrics**: See step counts, comparisons, and swaps
- **Synchronized Playback**: Step through algorithms together

## Export Features

- **Static Formats**: PNG, PDF, SVG
- **Animations**: GIF (animated algorithm steps)
- **Interactive**: HTML (interactive visualizations)
- **Multi-page PDF**: Export all steps as pages

## Examples

See the `examples/` directory for usage examples:

- `demo_playground.py` - Interactive playground usage
- `demo_interactive_controls.py` - Visualization controls
- `demo_comparison.py` - Algorithm comparison
- `demo_all_sorting.py` - Sorting algorithm demonstrations

## Philosophy

This platform is designed as a **visual learning playground** where users can:

- **See** how algorithms work step-by-step
- **Experiment** with different inputs and parameters
- **Compare** different approaches visually
- **Test** their own implementations
- **Learn** through visual understanding

Unlike LeetCode-style platforms, the focus is on **demonstration and exploration** rather than problem-solving exercises.

## Future Enhancements

- Additional advanced algorithms and data structures
- Enhanced tree and graph visualizations
- More playground environments
- Web interface (optional)
