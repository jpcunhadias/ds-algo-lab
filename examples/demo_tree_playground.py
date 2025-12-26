"""
Example: Tree Playground Demonstration
Demonstrates tree operations and traversals.
"""

from src.playground.tree_playground import TreePlayground


def main():
    """Demonstrate tree playground."""
    print("=" * 60)
    print("Tree Playground Demonstration")
    print("=" * 60)

    # Create BST playground
    print("\n1. Binary Search Tree (BST)")
    print("-" * 60)
    pg_bst = TreePlayground(tree_type="bst")

    # Insert values
    values = [50, 30, 70, 20, 40, 60, 80]
    print(f"Inserting values: {values}")
    for value in values:
        steps = pg_bst.insert(value)
        print(f"  Inserted {value}")

    print(f"\nTree size: {len(pg_bst.tree)}")
    print(f"In-order traversal: {pg_bst.tree.inorder_traversal()}")

    # Demonstrate traversals
    print("\n2. Tree Traversals")
    print("-" * 60)
    for traversal_type in ["inorder", "preorder", "postorder", "levelorder"]:
        traversal = getattr(pg_bst.tree, f"{traversal_type}_traversal")()
        print(f"{traversal_type.title()}: {traversal}")

    # Demonstrate search
    print("\n3. Search Operation")
    print("-" * 60)
    search_value = 40
    steps = pg_bst.search(search_value)
    print(f"Searching for {search_value}")
    pg_bst.visualize(steps, interactive=True)

    # Demonstrate AVL Tree
    print("\n4. AVL Tree")
    print("-" * 60)
    pg_avl = TreePlayground(tree_type="avl")
    avl_values = [10, 20, 30, 40, 50, 25]
    print(f"Inserting values: {avl_values}")
    for value in avl_values:
        steps = pg_avl.insert(value)
        print(f"  Inserted {value}")

    print(f"\nAVL Tree size: {len(pg_avl.tree)}")
    print(f"In-order traversal: {pg_avl.tree.inorder_traversal()}")

    # Visualize final AVL tree
    final_step = {
        "operation": "normal",
        "step_number": 1,
        "description": "Final AVL tree state",
        "data_structure": pg_avl.tree,
        "current_node": None,
        "highlighted_nodes": [],
    }
    pg_avl.visualize([final_step], interactive=True)


if __name__ == "__main__":
    main()

