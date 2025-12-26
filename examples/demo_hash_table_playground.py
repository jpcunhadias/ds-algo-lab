"""
Example: Hash Table Playground Demonstration
Demonstrates hash table operations and collision handling.
"""

from src.playground.hash_table_playground import HashTablePlayground


def main():
    """Demonstrate hash table playground."""
    print("=" * 60)
    print("Hash Table Playground Demonstration")
    print("=" * 60)

    # Create hash table
    pg = HashTablePlayground(initial_capacity=8, load_factor_threshold=0.75)

    print(f"Initial Capacity: {pg.hash_table.get_capacity()}")
    print(f"Load Factor Threshold: {pg.hash_table._load_factor_threshold}")

    # Insert values
    print("\n1. Insert Operations")
    print("-" * 60)
    keys = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    print(f"Inserting keys: {keys}")

    for key in keys:
        steps = pg.insert(key, f"value_{key}")
        print(f"  Inserted {key}:{pg.hash_table.get(key)}")
        print(f"    Size: {len(pg.hash_table)}, Load Factor: {pg.hash_table.get_load_factor():.2f}")

    # Visualize final state
    final_step = {
        "operation": "normal",
        "step_number": 1,
        "description": "Final hash table state",
        "data_structure": pg.hash_table,
    }
    pg.visualize([final_step], interactive=True)

    # Get operations
    print("\n2. Get Operations")
    print("-" * 60)
    for key in ["apple", "banana", "nonexistent"]:
        steps = pg.get(key)
        value = pg.hash_table.get(key)
        if value:
            print(f"  Found {key}: {value}")
        else:
            print(f"  Not found: {key}")

    # Delete operations
    print("\n3. Delete Operations")
    print("-" * 60)
    delete_key = "banana"
    steps = pg.delete(delete_key)
    print(f"  Deleted {delete_key}")
    print(f"    Size: {len(pg.hash_table)}, Load Factor: {pg.hash_table.get_load_factor():.2f}")

    # Verify deletion
    value = pg.hash_table.get(delete_key)
    if value:
        print(f"  ERROR: {delete_key} still exists!")
    else:
        print(f"  Verified: {delete_key} deleted successfully")

    # Demonstrate collision
    print("\n4. Collision Demonstration")
    print("-" * 60)
    pg2 = HashTablePlayground(initial_capacity=4, load_factor_threshold=1.0)
    collision_keys = ["key1", "key2", "key3", "key4", "key5"]
    print(f"Inserting keys into small table (capacity=4): {collision_keys}")
    for key in collision_keys:
        steps = pg2.insert(key, f"value_{key}")
        print(f"  Inserted {key}")

    print(f"\nFinal stats:")
    print(f"  Size: {len(pg2.hash_table)}")
    print(f"  Capacity: {pg2.hash_table.get_capacity()}")
    print(f"  Load Factor: {pg2.hash_table.get_load_factor():.2f}")

    final_step2 = {
        "operation": "normal",
        "step_number": 1,
        "description": "Hash table with collisions",
        "data_structure": pg2.hash_table,
    }
    pg2.visualize([final_step2], interactive=True)


if __name__ == "__main__":
    main()

