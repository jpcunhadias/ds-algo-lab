"""
CLI for launching playgrounds and demonstrations.
"""

from pathlib import Path
import click
from ..playground.sorting_playground import SortingPlayground
from ..playground.searching_playground import SearchingPlayground
from ..playground.input_builder import InputBuilder
from ..testing.implementation_tester import ImplementationTester
from ..templates.algorithm_templates import AlgorithmTemplates
from ..export.visualization_exporter import VisualizationExporter
from ..export.sharing import VisualizationSharing


@click.group()
def cli():
    """DSA Learning Playground - Visual Demonstration Platform"""
    pass


@cli.command()
@click.argument('playground_type', type=click.Choice(['sorting', 'searching']))
@click.option('--algorithm', '-a', help='Algorithm to run')
@click.option('--input', '-i', help='Input data (comma-separated)')
@click.option('--size', '-s', type=int, default=10, help='Input size for generated data')
@click.option('--type', '-t', type=click.Choice(['random', 'sorted', 'reversed', 'nearly_sorted']),
              default='random', help='Input type')
@click.option('--compare', is_flag=True, help='Compare multiple algorithms')
def playground(playground_type, algorithm, input, size, type, compare):
    """Launch an interactive playground."""
    if playground_type == 'sorting':
        pg = SortingPlayground()

        # Set input
        if input:
            input_data = [int(x.strip()) for x in input.split(',')]
        else:
            generators = pg.get_input_generators()
            input_data = generators[type](size)

        pg.set_input(input_data)
        print(f"Input: {input_data}")

        if compare:
            # Compare all algorithms
            algorithms = pg.get_available_algorithms()
            pg.compare_algorithms(algorithms)
        elif algorithm:
            # Run single algorithm
            steps = pg.run_algorithm(algorithm)
            pg.visualize(steps, interactive=True)
        else:
            # Interactive mode
            print("\nAvailable algorithms:", ", ".join(pg.get_available_algorithms()))
            algo = click.prompt("Select algorithm", type=click.Choice(pg.get_available_algorithms()))
            steps = pg.run_algorithm(algo)
            pg.visualize(steps, interactive=True)

    elif playground_type == 'searching':
        pg = SearchingPlayground()

        # Set input (must be sorted for binary search)
        if input:
            input_data = [int(x.strip()) for x in input.split(',')]
        else:
            from ..playground.base import InputGenerator
            input_data = InputGenerator.sorted_array(size, start=1, step=2)

        pg.set_input(input_data)

        target = click.prompt("Enter target value", type=int)
        pg.set_target(target)

        print(f"Input: {input_data}")
        print(f"Target: {target}")

        if algorithm:
            steps = pg.run_algorithm(algorithm)
            pg.visualize(steps, interactive=True)
        else:
            print("\nAvailable algorithms:", ", ".join(pg.get_available_algorithms()))
            algo = click.prompt("Select algorithm", type=click.Choice(pg.get_available_algorithms()))
            steps = pg.run_algorithm(algo)
            pg.visualize(steps, interactive=True)


@cli.command()
@click.argument('algorithm_name')
@click.option('--size', '-s', type=int, default=10, help='Input size')
@click.option('--type', '-t', type=click.Choice(['random', 'sorted', 'reversed']),
              default='random', help='Input type')
def demo(algorithm_name, size, type):
    """Run a quick demonstration of an algorithm."""
    if 'sort' in algorithm_name.lower():
        pg = SortingPlayground()
        pg.demo(algorithm_name, size, type)
    elif 'search' in algorithm_name.lower():
        pg = SearchingPlayground()
        pg.demo(algorithm_name, size)
    else:
        click.echo(f"Unknown algorithm: {algorithm_name}")


@cli.command()
@click.argument('algorithm1')
@click.argument('algorithm2')
@click.option('--size', '-s', type=int, default=10, help='Input size')
@click.option('--type', '-t', type=click.Choice(['random', 'sorted', 'reversed']),
              default='random', help='Input type')
def compare(algorithm1, algorithm2, size, type):
    """Compare two algorithms side-by-side."""
    from ..playground.base import InputGenerator

    pg = SortingPlayground()

    # Generate input
    generators = pg.get_input_generators()
    input_data = generators[type](size)
    pg.set_input(input_data)

    print(f"Comparing {algorithm1} vs {algorithm2}")
    print(f"Input: {input_data}\n")

    pg.compare_algorithms([algorithm1, algorithm2])


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--function', '-f', help='Function name to test')
@click.option('--input', '-i', help='Input data (comma-separated)')
@click.option('--target', '-t', help='Target value (for searching)')
def test(file_path, function, input, target):
    """Test a user implementation with visualization."""
    tester = ImplementationTester()

    # Read code
    code = Path(file_path).read_text()

    # Parse input
    if input:
        input_data = [int(x.strip()) for x in input.split(',')]
    else:
        input_data = [64, 34, 25, 12, 22, 11, 90]  # Default

    # Determine algorithm type
    if 'search' in function.lower() if function else 'search' in code.lower():
        if target is None:
            target = input_data[len(input_data) // 2]  # Default target
        result = tester.test_searching_implementation(
            code, function or 'linear_search', input_data, int(target)
        )
    else:
        result = tester.test_sorting_implementation(
            code, function or 'bubble_sort', input_data
        )

    # Display results
    if result['success']:
        click.echo(f"✓ Code executed successfully")
        if result.get('correct'):
            click.echo(f"✓ Result is correct!")
        else:
            click.echo(f"✗ Result is incorrect")
            click.echo(f"  Expected: {result.get('expected')}")
            click.echo(f"  Got: {result.get('output')}")

        if result.get('visualization'):
            click.echo("\nShowing visualization...")
            import matplotlib.pyplot as plt
            viz = result['visualization']
            if 'figure' in viz:
                plt.show()
    else:
        click.echo(f"✗ Error: {result.get('error')}")


@cli.command()
@click.argument('algorithm_name')
def template(algorithm_name):
    """Get a code template for an algorithm."""
    template = AlgorithmTemplates.get_template(algorithm_name)
    if template:
        click.echo(template)
    else:
        click.echo(f"Template not available for: {algorithm_name}")
        click.echo(f"Available templates: {', '.join(AlgorithmTemplates.list_templates())}")


@cli.command()
@click.argument('file_path')
@click.option('--format', '-f', type=click.Choice(['png', 'pdf', 'svg', 'gif', 'html']),
              default='png', help='Export format')
@click.option('--animation', is_flag=True, help='Export as animation')
def export(file_path, format, animation):
    """Export visualization to file."""
    click.echo("Export functionality - use playground commands to generate visualizations first")
    click.echo(f"Format: {format}, Animation: {animation}")


@cli.command()
def list_algorithms():
    """List all available algorithms."""
    pg_sort = SortingPlayground()
    pg_search = SearchingPlayground()

    click.echo("\nSorting Algorithms:")
    for algo in pg_sort.get_available_algorithms():
        click.echo(f"  - {algo}")

    click.echo("\nSearching Algorithms:")
    for algo in pg_search.get_available_algorithms():
        click.echo(f"  - {algo}")


def main():
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()

