"""
Example: Graph Playground Demonstration
Demonstrates graph operations and BFS/DFS algorithms.
"""

from src.playground.graph_playground import GraphPlayground


def main():
    """Demonstrate graph playground."""
    print("=" * 60)
    print("Graph Playground Demonstration")
    print("=" * 60)

    # Create undirected graph
    print("\n1. Undirected Graph")
    print("-" * 60)
    pg = GraphPlayground(directed=False)

    # Add vertices
    vertices = ["A", "B", "C", "D", "E", "F"]
    print(f"Adding vertices: {vertices}")
    for vertex in vertices:
        pg.graph.add_vertex(vertex)

    # Add edges
    edges = [
        ("A", "B"),
        ("A", "C"),
        ("B", "D"),
        ("C", "D"),
        ("D", "E"),
        ("E", "F"),
    ]
    print(f"Adding edges: {edges}")
    for from_v, to_v in edges:
        pg.graph.add_edge(from_v, to_v)

    print(f"\nGraph vertices: {pg.graph.get_vertices()}")
    print(f"Graph edges: {pg.graph.get_edges()}")

    # Demonstrate BFS
    print("\n2. Breadth-First Search (BFS)")
    print("-" * 60)
    start_vertex = "A"
    print(f"Running BFS from vertex {start_vertex}")
    steps = pg.run_bfs(start_vertex)
    print(f"Total steps: {len(steps)}")
    pg.visualize(steps, interactive=True)

    # Demonstrate DFS
    print("\n3. Depth-First Search (DFS)")
    print("-" * 60)
    print(f"Running DFS from vertex {start_vertex}")
    steps = pg.run_dfs(start_vertex)
    print(f"Total steps: {len(steps)}")
    pg.visualize(steps, interactive=True)

    # Create directed graph
    print("\n4. Directed Graph")
    print("-" * 60)
    pg_directed = GraphPlayground(directed=True)

    vertices = ["1", "2", "3", "4"]
    for vertex in vertices:
        pg_directed.graph.add_vertex(vertex)

    directed_edges = [
        ("1", "2"),
        ("1", "3"),
        ("2", "4"),
        ("3", "4"),
    ]
    for from_v, to_v in directed_edges:
        pg_directed.graph.add_edge(from_v, to_v)

    print(f"Directed graph vertices: {pg_directed.graph.get_vertices()}")
    print(f"Directed graph edges: {pg_directed.graph.get_edges()}")

    steps = pg_directed.run_bfs("1")
    pg_directed.visualize(steps, interactive=True)


if __name__ == "__main__":
    main()

