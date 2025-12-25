"""
Framework for testing user implementations with visualization.
"""

import ast
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from typing import Any, Dict, List, Optional, Callable
from ..data_structures.array import Array
from ..visualization.algo_visualizer import AlgorithmVisualizer
from ..visualization.interactive_controls import InteractiveControls


class ImplementationTester:
    """
    Test user implementations and generate visualizations.
    """

    def __init__(self):
        """Initialize the tester."""
        self._allowed_modules = {'math', 'collections', 'itertools'}
        self._allowed_builtins = {
            'abs', 'all', 'any', 'bool', 'dict', 'enumerate', 'filter',
            'float', 'int', 'len', 'list', 'map', 'max', 'min', 'range',
            'reversed', 'sorted', 'str', 'sum', 'tuple', 'zip'
        }

    def test_sorting_implementation(
        self,
        code: str,
        function_name: str,
        input_data: List[Any],
        visualize: bool = True
    ) -> Dict[str, Any]:
        """
        Test a sorting algorithm implementation.

        Args:
            code: Python code string
            function_name: Name of the sorting function
            input_data: Input array to sort
            visualize: Whether to visualize the execution

        Returns:
            Dictionary with test results
        """
        try:
            # Parse and validate code
            tree = ast.parse(code)
            self._validate_ast(tree)

            # Execute code safely
            namespace = self._create_safe_namespace()
            exec(code, namespace)

            if function_name not in namespace:
                return {
                    'success': False,
                    'error': f"Function '{function_name}' not found in code",
                    'visualization': None,
                }

            func = namespace[function_name]

            # Create array and run algorithm
            arr = Array(input_data.copy())
            original_data = input_data.copy()

            # Execute function
            result = func(arr.to_list())

            # Check if result is correct
            expected = sorted(original_data)
            is_correct = result == expected

            # Generate visualization if requested
            visualization = None
            if visualize:
                # Try to extract steps from execution
                # For now, create a simple visualization
                visualization = self._create_simple_visualization(
                    original_data, result, is_correct
                )

            return {
                'success': True,
                'correct': is_correct,
                'input': original_data,
                'output': result,
                'expected': expected,
                'visualization': visualization,
            }

        except SyntaxError as e:
            return {
                'success': False,
                'error': f"Syntax error: {str(e)}",
                'visualization': None,
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Execution error: {str(e)}",
                'visualization': None,
            }

    def test_searching_implementation(
        self,
        code: str,
        function_name: str,
        input_data: List[Any],
        target: Any,
        visualize: bool = True
    ) -> Dict[str, Any]:
        """
        Test a searching algorithm implementation.

        Args:
            code: Python code string
            function_name: Name of the searching function
            input_data: Input array to search in
            target: Target value to search for
            visualize: Whether to visualize the execution

        Returns:
            Dictionary with test results
        """
        try:
            # Parse and validate code
            tree = ast.parse(code)
            self._validate_ast(tree)

            # Execute code safely
            namespace = self._create_safe_namespace()
            exec(code, namespace)

            if function_name not in namespace:
                return {
                    'success': False,
                    'error': f"Function '{function_name}' not found in code",
                    'visualization': None,
                }

            func = namespace[function_name]

            # Execute function
            result = func(input_data, target)

            # Check if result is correct
            expected_index = input_data.index(target) if target in input_data else -1
            is_correct = result == expected_index

            # Generate visualization if requested
            visualization = None
            if visualize:
                visualization = self._create_search_visualization(
                    input_data, target, result, is_correct
                )

            return {
                'success': True,
                'correct': is_correct,
                'input': input_data,
                'target': target,
                'output': result,
                'expected': expected_index,
                'visualization': visualization,
            }

        except SyntaxError as e:
            return {
                'success': False,
                'error': f"Syntax error: {str(e)}",
                'visualization': None,
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Execution error: {str(e)}",
                'visualization': None,
            }

    def _validate_ast(self, tree: ast.AST) -> None:
        """Validate AST for unsafe operations."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    if module and not module.startswith('.') and module not in self._allowed_modules:
                        if not module.startswith('src'):
                            raise ValueError(f"Import of '{module}' is not allowed")
                else:
                    for alias in node.names:
                        if alias.name and not alias.name.startswith('.') and alias.name not in self._allowed_modules:
                            if not alias.name.startswith('src'):
                                raise ValueError(f"Import of '{alias.name}' is not allowed")

            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ('open', 'exec', 'eval', '__import__'):
                        raise ValueError(f"Use of '{node.func.id}' is not allowed")

    def _create_safe_namespace(self) -> Dict[str, Any]:
        """Create safe namespace for code execution."""
        namespace = {
            '__builtins__': {
                name: getattr(__builtins__, name)
                for name in self._allowed_builtins
                if hasattr(__builtins__, name)
            }
        }

        for module_name in self._allowed_modules:
            try:
                namespace[module_name] = __import__(module_name)
            except ImportError:
                pass

        return namespace

    def _create_simple_visualization(
        self, original: List[Any], result: List[Any], is_correct: bool
    ) -> Dict[str, Any]:
        """Create a simple visualization of sorting result."""
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # Original array
        for i, val in enumerate(original):
            rect = patches.Rectangle(
                (i - 0.4, 0), 0.8, val,
                linewidth=2, edgecolor='black', facecolor='lightblue'
            )
            ax1.add_patch(rect)
            ax1.text(i, val/2, str(val), ha='center', va='center', fontweight='bold')

        ax1.set_xlim(-1, len(original))
        ax1.set_ylim(0, max(original) + 1)
        ax1.set_title('Original Array', fontweight='bold')
        ax1.set_aspect('equal')

        # Result array
        color = 'lightgreen' if is_correct else 'lightcoral'
        for i, val in enumerate(result):
            rect = patches.Rectangle(
                (i - 0.4, 0), 0.8, val,
                linewidth=2, edgecolor='black', facecolor=color
            )
            ax2.add_patch(rect)
            ax2.text(i, val/2, str(val), ha='center', va='center', fontweight='bold')

        ax2.set_xlim(-1, len(result))
        ax2.set_ylim(0, max(result) + 1 if result else 1)
        status = 'Correct!' if is_correct else 'Incorrect'
        ax2.set_title(f'Sorted Array ({status})', fontweight='bold')
        ax2.set_aspect('equal')

        plt.tight_layout()
        return {'figure': fig, 'axes': [ax1, ax2]}

    def _create_search_visualization(
        self, arr: List[Any], target: Any, result: int, is_correct: bool
    ) -> Dict[str, Any]:
        """Create visualization of search result."""
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches

        fig, ax = plt.subplots(figsize=(10, 4))

        for i, val in enumerate(arr):
            color = 'lightgreen' if i == result and is_correct else 'lightblue'
            if val == target:
                color = 'yellow'

            rect = patches.Rectangle(
                (i - 0.4, 0), 0.8, 1,
                linewidth=2, edgecolor='black', facecolor=color
            )
            ax.add_patch(rect)
            ax.text(i, 0.5, str(val), ha='center', va='center', fontweight='bold')

        ax.set_xlim(-1, len(arr))
        ax.set_ylim(-0.5, 1.5)
        ax.set_title(f'Searching for {target} - Found at index {result}', fontweight='bold')
        ax.set_aspect('equal')

        plt.tight_layout()
        return {'figure': fig, 'axes': [ax]}

