"""
CLI for launching playgrounds and demonstrations.
"""

from pathlib import Path

import click

from ..playground.searching_playground import SearchingPlayground
from ..playground.sorting_playground import SortingPlayground
from ..templates.algorithm_templates import AlgorithmTemplates
from ..testing.implementation_tester import ImplementationTester


@click.group()
def cli():
    """DSA Learning Playground - Visual Demonstration Platform"""
    pass


@cli.command()
@click.argument(
    "playground_type",
    type=click.Choice(["sorting", "searching", "tree", "graph", "hash_table"]),
)
@click.option("--algorithm", "-a", help="Algorithm to run")
@click.option("--input", "-i", help="Input data (comma-separated)")
@click.option(
    "--size", "-s", type=int, default=10, help="Input size for generated data"
)
@click.option(
    "--type",
    "-t",
    type=click.Choice(
        ["random", "sorted", "reversed", "nearly_sorted", "binary_tree", "bst", "avl"]
    ),
    default="random",
    help="Input type",
)
@click.option("--compare", is_flag=True, help="Compare multiple algorithms")
@click.option(
    "--directed", is_flag=True, help="Create directed graph (for graph playground)"
)
@click.option(
    "--traversal",
    help="Traversal type for tree (inorder, preorder, postorder, levelorder)",
)
@click.option("--start-vertex", help="Start vertex for graph algorithms")
@click.option("--skip-init", is_flag=True, help="Skip initialization visualization")
@click.option(
    "--init-interactive",
    is_flag=True,
    default=True,
    help="Use interactive mode for initialization visualization (default: True)",
)
def playground(
    playground_type,
    algorithm,
    input,
    size,
    type,
    compare,
    directed,
    traversal,
    start_vertex,
    skip_init,
    init_interactive,
):
    """Launch an interactive playground."""
    if playground_type == "sorting":
        pg = SortingPlayground()

        # Set input
        if input:
            input_data = [int(x.strip()) for x in input.split(",")]
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
            algo = click.prompt(
                "Select algorithm", type=click.Choice(pg.get_available_algorithms())
            )
            steps = pg.run_algorithm(algo)
            pg.visualize(steps, interactive=True)

    elif playground_type == "searching":
        pg = SearchingPlayground()

        # Set input (must be sorted for binary search)
        if input:
            input_data = [int(x.strip()) for x in input.split(",")]
        else:
            from ..playground.base import InputGenerator

            input_data = InputGenerator.sorted_array(size, start=1, step=2)

        pg.set_input(input_data)

        # Show input first, then ask for target
        print(f"Input array: {input_data}")
        print(f"Array length: {len(input_data)}")

        target = click.prompt("Enter target value to search for", type=int)
        pg.set_target(target)

        print(f"Target: {target}")

        if algorithm:
            steps = pg.run_algorithm(algorithm)
            pg.visualize(steps, interactive=True)
        else:
            print("\nAvailable algorithms:", ", ".join(pg.get_available_algorithms()))
            algo = click.prompt(
                "Select algorithm", type=click.Choice(pg.get_available_algorithms())
            )
            steps = pg.run_algorithm(algo)
            pg.visualize(steps, interactive=True)

    elif playground_type == "tree":
        from ..playground.tree_playground import TreePlayground

        tree_type = type if type in ["binary_tree", "bst", "avl"] else "bst"
        pg = TreePlayground(tree_type=tree_type)

        # Set input
        if input:
            input_data = [x.strip() for x in input.split(",")]
            # Try to convert to integers if possible
            try:
                input_data = [int(x) for x in input_data]
            except ValueError:
                pass
        else:
            import random

            input_data = random.sample(range(1, 20), size)

        pg.set_input(input_data, show_initialization=not skip_init)
        print(f"Tree Type: {tree_type}")
        print(f"Input: {input_data}")

        # If initialization was shown, the operation menu will appear automatically
        # Don't show CLI menu again unless explicitly requested
        if not skip_init:
            # Initialization was shown, operation menu will appear via callback
            # Exit here to avoid showing duplicate menu
            return

        if algorithm:
            # Run operation
            if algorithm == "traverse":
                traversal_type = traversal or "inorder"
                steps = pg.traverse(traversal_type)
            elif algorithm == "insert":
                value = click.prompt("Enter value to insert", type=int)
                steps = pg.insert(value)
            elif algorithm == "delete":
                value = click.prompt("Enter value to delete", type=int)
                steps = pg.delete(value)
            elif algorithm == "search":
                value = click.prompt("Enter value to search", type=int)
                steps = pg.search(value)
            else:
                click.echo(f"Unknown operation: {algorithm}")
                return
            pg.visualize(steps, interactive=True)
        else:
            # Interactive mode
            print("\nAvailable operations:", ", ".join(pg.get_available_algorithms()))
            op = click.prompt(
                "Select operation", type=click.Choice(pg.get_available_algorithms())
            )
            if op == "traverse":
                traversal_type = click.prompt(
                    "Traversal type",
                    type=click.Choice(
                        ["inorder", "preorder", "postorder", "levelorder"]
                    ),
                    default="inorder",
                )
                steps = pg.traverse(traversal_type)
            elif op == "insert":
                value = click.prompt("Enter value to insert", type=int)
                steps = pg.insert(value)
            elif op == "delete":
                value = click.prompt("Enter value to delete", type=int)
                steps = pg.delete(value)
            elif op == "search":
                value = click.prompt("Enter value to search", type=int)
                steps = pg.search(value)
            pg.visualize(steps, interactive=True)

    elif playground_type == "graph":
        from ..playground.graph_playground import GraphPlayground

        pg = GraphPlayground(directed=directed)

        # Create sample graph or use provided vertices
        if input:
            vertices = [x.strip() for x in input.split(",")]
        else:
            vertices = ["A", "B", "C", "D", "E"]

        # Set input (which will add vertices and show initialization if not skipped)
        pg.set_input(vertices, show_initialization=not skip_init)

        # Add some default edges if none provided
        if len(vertices) >= 2:
            for i in range(len(vertices) - 1):
                pg.graph.add_edge(vertices[i], vertices[i + 1])

        print(f"Graph Type: {'Directed' if directed else 'Undirected'}")
        print(f"Vertices: {vertices}")

        if algorithm:
            # Run algorithm
            start = start_vertex or vertices[0]
            if algorithm == "bfs":
                steps = pg.run_bfs(start)
            elif algorithm == "dfs":
                steps = pg.run_dfs(start)
            else:
                click.echo(f"Unknown algorithm: {algorithm}")
                return
            pg.visualize(steps, interactive=True)
        else:
            # Interactive mode
            print("\nAvailable algorithms:", ", ".join(pg.get_available_algorithms()))
            algo = click.prompt(
                "Select algorithm", type=click.Choice(pg.get_available_algorithms())
            )
            start = start_vertex or click.prompt(
                "Enter start vertex", default=vertices[0]
            )
            if algo == "bfs":
                steps = pg.run_bfs(start)
            elif algo == "dfs":
                steps = pg.run_dfs(start)
            pg.visualize(steps, interactive=True)

    elif playground_type == "hash_table":
        from ..playground.hash_table_playground import HashTablePlayground

        pg = HashTablePlayground()

        # Set input
        if input:
            input_data = [x.strip() for x in input.split(",")]
        else:
            import random

            input_data = [f"key{i}" for i in range(1, size + 1)]

        pg.set_input(input_data, show_initialization=not skip_init)
        print(f"Hash Table Capacity: {pg.hash_table.get_capacity()}")
        print(f"Input keys: {input_data}")

        if algorithm:
            # Run operation
            if algorithm == "insert":
                if input_data:
                    for key in input_data:
                        steps = pg.insert(key, f"value_{key}")
                        pg.visualize(steps, interactive=False)
                else:
                    key = click.prompt("Enter key to insert")
                    value = click.prompt("Enter value", default=key)
                    steps = pg.insert(key, value)
                    pg.visualize(steps, interactive=True)
            elif algorithm == "get":
                key = click.prompt("Enter key to get")
                steps = pg.get(key)
                pg.visualize(steps, interactive=True)
            elif algorithm == "delete":
                key = click.prompt("Enter key to delete")
                steps = pg.delete(key)
                pg.visualize(steps, interactive=True)
            else:
                click.echo(f"Unknown operation: {algorithm}")
                return
        else:
            # Interactive mode - input already set with initialization visualization
            print("\nHash Table Stats:")
            print(f"  Size: {len(pg.hash_table)}")
            print(f"  Capacity: {pg.hash_table.get_capacity()}")
            print(f"  Load Factor: {pg.hash_table.get_load_factor():.2f}")

            print("\nAvailable operations:", ", ".join(pg.get_available_algorithms()))
            op = click.prompt(
                "Select operation", type=click.Choice(pg.get_available_algorithms())
            )
            if op == "insert":
                key = click.prompt("Enter key to insert")
                value = click.prompt("Enter value", default=key)
                steps = pg.insert(key, value)
            elif op == "get":
                key = click.prompt("Enter key to get")
                steps = pg.get(key)
            elif op == "delete":
                key = click.prompt("Enter key to delete")
                steps = pg.delete(key)
            pg.visualize(steps, interactive=True)


@cli.command()
@click.argument("algorithm_name")
@click.option("--size", "-s", type=int, default=10, help="Input size")
@click.option(
    "--type",
    "-t",
    type=click.Choice(["random", "sorted", "reversed"]),
    default="random",
    help="Input type",
)
def demo(algorithm_name, size, type):
    """Run a quick demonstration of an algorithm."""
    if "sort" in algorithm_name.lower():
        pg = SortingPlayground()
        pg.demo(algorithm_name, size, type)
    elif "search" in algorithm_name.lower():
        pg = SearchingPlayground()
        pg.demo(algorithm_name, size)
    else:
        click.echo(f"Unknown algorithm: {algorithm_name}")


@cli.command()
@click.argument("algorithm1")
@click.argument("algorithm2")
@click.option("--size", "-s", type=int, default=10, help="Input size")
@click.option(
    "--type",
    "-t",
    type=click.Choice(["random", "sorted", "reversed"]),
    default="random",
    help="Input type",
)
def compare(algorithm1, algorithm2, size, type):
    """Compare two algorithms side-by-side."""

    pg = SortingPlayground()

    # Generate input
    generators = pg.get_input_generators()
    input_data = generators[type](size)
    pg.set_input(input_data)

    print(f"Comparing {algorithm1} vs {algorithm2}")
    print(f"Input: {input_data}\n")

    pg.compare_algorithms([algorithm1, algorithm2])


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--function", "-f", help="Function name to test")
@click.option("--input", "-i", help="Input data (comma-separated)")
@click.option("--target", "-t", help="Target value (for searching)")
def test(file_path, function, input, target):
    """Test a user implementation with visualization."""
    tester = ImplementationTester()

    # Read code
    code = Path(file_path).read_text()

    # Parse input
    if input:
        input_data = [int(x.strip()) for x in input.split(",")]
    else:
        input_data = [64, 34, 25, 12, 22, 11, 90]  # Default

    # Determine algorithm type
    if "search" in function.lower() if function else "search" in code.lower():
        if target is None:
            target = input_data[len(input_data) // 2]  # Default target
        result = tester.test_searching_implementation(
            code, function or "linear_search", input_data, int(target)
        )
    else:
        result = tester.test_sorting_implementation(
            code, function or "bubble_sort", input_data
        )

    # Display results
    if result["success"]:
        click.echo("✓ Code executed successfully")
        if result.get("correct"):
            click.echo("✓ Result is correct!")
        else:
            click.echo("✗ Result is incorrect")
            click.echo(f"  Expected: {result.get('expected')}")
            click.echo(f"  Got: {result.get('output')}")

        if result.get("visualization"):
            click.echo("\nShowing visualization...")
            import matplotlib.pyplot as plt

            viz = result["visualization"]
            if "figure" in viz:
                plt.show()
    else:
        click.echo(f"✗ Error: {result.get('error')}")


@cli.command()
@click.argument("algorithm_name")
def template(algorithm_name):
    """Get a code template for an algorithm."""
    template = AlgorithmTemplates.get_template(algorithm_name)
    if template:
        click.echo(template)
    else:
        click.echo(f"Template not available for: {algorithm_name}")
        click.echo(
            f"Available templates: {', '.join(AlgorithmTemplates.list_templates())}"
        )


@cli.command()
@click.argument("file_path")
@click.option(
    "--format",
    "-f",
    type=click.Choice(["png", "pdf", "svg", "gif", "html"]),
    default="png",
    help="Export format",
)
@click.option("--animation", is_flag=True, help="Export as animation")
def export(file_path, format, animation):
    """Export visualization to file."""
    click.echo(
        "Export functionality - use playground commands to generate visualizations first"
    )
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

    click.echo("\nGraph Algorithms:")
    from ..playground.graph_playground import GraphPlayground

    pg_graph = GraphPlayground()
    for algo in pg_graph.get_available_algorithms():
        click.echo(f"  - {algo}")


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
