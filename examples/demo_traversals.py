"""
Example: Traversal Demonstrations
Demonstrates tree and graph traversals.
"""

from src.playground.tree_playground import TreePlayground
from src.playground.graph_playground import GraphPlayground


def main():
    """Demonstrate traversals."""
    print("=" * 60)
    print("Traversal Demonstrations")
    print("=" * 60)

    # Tree traversals
    print("\n1. Tree Traversals")
    print("-" * 60)
    pg = TreePlayground(tree_type="bst")

    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    print(f"Building BST with values: {values}")
    for value in values:
        pg.tree.insert(value)

    print(f"\nTree size: {len(pg.tree)}")

    # Demonstrate all traversals
    traversal_types = ["inorder", "preorder", "postorder", "levelorder"]
    for traversal_type in traversal_types:
        print(f"\n{traversal_type.upper()} Traversal:")
        steps = pg.traverse(traversal_type)
        print(f"  Order: {[step['current_node'] for step in steps if step.get('current_node')]}")
        # Visualize first few steps
        if len(steps) <= 5:
            pg.visualize(steps, interactive=True)
        else:
            # Show first and last step
            pg.visualize([steps[0], steps[-1]], interactive=True)

    # Graph traversals
    print("\n2. Graph Traversals")
    print("-" * 60)
    pg_graph = GraphPlayground(directed=False)

    vertices = ["A", "B", "C", "D", "E"]
    edges = [
        ("A", "B"),
        ("A", "C"),
        ("B", "D"),
        ("C", "D"),
        ("D", "E"),
    ]

    print(f"Creating graph with vertices: {vertices}")
    print(f"Edges: {edges}")

    for vertex in vertices:
        pg_graph.graph.add_vertex(vertex)
    for from_v, to_v in edges:
        pg_graph.graph.add_edge(from_v, to_v)

    # BFS
    print("\nBFS Traversal from A:")
    steps_bfs = pg_graph.run_bfs("A")
    traversal_order = [step.get("current_vertex") for step in steps_bfs if step.get("current_vertex")]
    print(f"  Order: {traversal_order}")
    pg_graph.visualize(steps_bfs, interactive=True)

    # DFS
    print("\nDFS Traversal from A:")
    steps_dfs = pg_graph.run_dfs("A")
    traversal_order = [step.get("current_vertex") for step in steps_dfs if step.get("current_vertex")]
    print(f"  Order: {traversal_order}")
    pg_graph.visualize(steps_dfs, interactive=True)


if __name__ == "__main__":
    main()

