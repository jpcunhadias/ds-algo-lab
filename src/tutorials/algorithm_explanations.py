"""
Algorithm Explanations
Detailed explanations and educational content for algorithms.
"""

from typing import Dict, List, Optional


class AlgorithmExplanation:
    """Stores detailed explanation for an algorithm."""

    def __init__(
        self,
        name: str,
        overview: str,
        how_it_works: str,
        key_concepts: List[str],
        complexity: Dict[str, str],
        use_cases: List[str],
        advantages: List[str],
        disadvantages: List[str],
        tips: List[str] = None,
        common_pitfalls: List[str] = None,
    ):
        """
        Initialize algorithm explanation.

        Args:
            name: Algorithm name
            overview: Brief overview
            how_it_works: Detailed explanation of how it works
            key_concepts: List of key concepts
            complexity: Dictionary with 'time' and 'space' keys
            use_cases: List of use cases
            advantages: List of advantages
            disadvantages: List of disadvantages
            tips: List of tips (optional)
            common_pitfalls: List of common pitfalls (optional)
        """
        self.name = name
        self.overview = overview
        self.how_it_works = how_it_works
        self.key_concepts = key_concepts
        self.complexity = complexity
        self.use_cases = use_cases
        self.advantages = advantages
        self.disadvantages = disadvantages
        self.tips = tips or []
        self.common_pitfalls = common_pitfalls or []


class AlgorithmExplanations:
    """Collection of algorithm explanations."""

    EXPLANATIONS: Dict[str, AlgorithmExplanation] = {
        "Bubble Sort": AlgorithmExplanation(
            name="Bubble Sort",
            overview="A simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
            how_it_works="The algorithm works by repeatedly swapping adjacent elements if they are in the wrong order. This process continues until no more swaps are needed, indicating the list is sorted. The name 'bubble sort' comes from the way smaller elements 'bubble' to the top of the list.",
            key_concepts=[
                "Adjacent comparison",
                "Repeated passes",
                "Early termination when no swaps occur",
            ],
            complexity={"time": "O(n²)", "space": "O(1)"},
            use_cases=[
                "Educational purposes",
                "Small datasets",
                "When simplicity is more important than efficiency",
            ],
            advantages=[
                "Simple to understand and implement",
                "In-place sorting (O(1) space)",
                "Stable (maintains relative order of equal elements)",
                "Can detect if list is already sorted",
            ],
            disadvantages=[
                "Very slow for large datasets",
                "O(n²) time complexity",
                "Many unnecessary comparisons",
            ],
            tips=[
                "Use early termination to optimize",
                "Not suitable for production code with large datasets",
                "Good for learning sorting concepts",
            ],
            common_pitfalls=[
                "Forgetting to check if array is already sorted",
                "Off-by-one errors in loop bounds",
                "Not updating swapped flag correctly",
            ],
        ),
        "Insertion Sort": AlgorithmExplanation(
            name="Insertion Sort",
            overview="Builds the final sorted array one item at a time by inserting each element into its correct position in the sorted portion.",
            how_it_works="The algorithm maintains a sorted subarray at the beginning. For each new element, it finds the correct position in the sorted subarray and inserts it there, shifting other elements as needed.",
            key_concepts=[
                "Sorted subarray",
                "Insertion and shifting",
                "Adaptive (efficient for nearly sorted data)",
            ],
            complexity={"time": "O(n²)", "space": "O(1)"},
            use_cases=[
                "Small datasets",
                "Nearly sorted data",
                "When simplicity is important",
            ],
            advantages=[
                "Simple implementation",
                "Efficient for small or nearly sorted data",
                "In-place sorting",
                "Stable",
                "Adaptive (O(n) for nearly sorted data)",
            ],
            disadvantages=[
                "O(n²) worst case",
                "Inefficient for large datasets",
            ],
            tips=[
                "Very efficient for small arrays (< 10-20 elements)",
                "Good choice when data is already partially sorted",
                "Used internally by more complex algorithms",
            ],
        ),
        "Selection Sort": AlgorithmExplanation(
            name="Selection Sort",
            overview="Repeatedly finds the minimum element from the unsorted portion and places it at the beginning.",
            how_it_works="The algorithm divides the array into sorted and unsorted parts. It repeatedly finds the minimum element from the unsorted part and swaps it with the first element of the unsorted part.",
            key_concepts=[
                "Finding minimum",
                "Swapping to correct position",
                "Dividing array into sorted/unsorted parts",
            ],
            complexity={"time": "O(n²)", "space": "O(1)"},
            use_cases=[
                "Small datasets",
                "When memory writes are expensive",
            ],
            advantages=[
                "Simple to implement",
                "In-place sorting",
                "Minimal memory writes (O(n) swaps)",
            ],
            disadvantages=[
                "O(n²) time complexity",
                "Not stable",
                "Not adaptive",
            ],
            tips=[
                "Useful when write operations are expensive",
                "Not recommended for large datasets",
            ],
        ),
        "Merge Sort": AlgorithmExplanation(
            name="Merge Sort",
            overview="A divide-and-conquer algorithm that divides the array into halves, sorts them, and merges them back together.",
            how_it_works="The algorithm recursively divides the array into two halves until each half contains one element. Then it merges the halves back together in sorted order. The merge process compares elements from both halves and places them in the correct order.",
            key_concepts=[
                "Divide and conquer",
                "Recursion",
                "Merging sorted arrays",
            ],
            complexity={"time": "O(n log n)", "space": "O(n)"},
            use_cases=[
                "Large datasets",
                "When stability is required",
                "External sorting",
            ],
            advantages=[
                "Consistent O(n log n) performance",
                "Stable",
                "Predictable performance",
            ],
            disadvantages=[
                "Requires O(n) extra space",
                "Not in-place",
                "Slower than quicksort in practice",
            ],
            tips=[
                "Excellent for large datasets",
                "Good choice when stability matters",
                "Used in many standard library implementations",
            ],
        ),
        "Quick Sort": AlgorithmExplanation(
            name="Quick Sort",
            overview="A divide-and-conquer algorithm that picks a pivot element and partitions the array around the pivot.",
            how_it_works="The algorithm selects a pivot element and rearranges the array so that all elements smaller than the pivot are on the left and all elements greater are on the right. It then recursively sorts the left and right subarrays.",
            key_concepts=[
                "Pivot selection",
                "Partitioning",
                "Divide and conquer",
            ],
            complexity={"time": "O(n log n) average, O(n²) worst", "space": "O(log n)"},
            use_cases=[
                "General-purpose sorting",
                "Large datasets",
                "When average performance matters",
            ],
            advantages=[
                "Very fast average case",
                "In-place (with proper implementation)",
                "Cache-friendly",
            ],
            disadvantages=[
                "O(n²) worst case",
                "Not stable",
                "Pivot selection affects performance",
            ],
            tips=[
                "Choose good pivot (median of three)",
                "Use insertion sort for small subarrays",
                "Most widely used sorting algorithm",
            ],
        ),
        "Binary Search": AlgorithmExplanation(
            name="Binary Search",
            overview="Searches a sorted array by repeatedly dividing the search interval in half.",
            how_it_works="The algorithm compares the target value with the middle element. If they match, the search is complete. Otherwise, it eliminates half of the search space based on the comparison and continues with the remaining half.",
            key_concepts=[
                "Requires sorted array",
                "Divide and conquer",
                "Eliminating half the search space",
            ],
            complexity={"time": "O(log n)", "space": "O(1)"},
            use_cases=[
                "Searching in sorted arrays",
                "Finding insertion points",
                "Range queries",
            ],
            advantages=[
                "Very efficient O(log n)",
                "Simple to implement",
                "Low space complexity",
            ],
            disadvantages=[
                "Requires sorted array",
                "Not suitable for unsorted data",
            ],
            tips=[
                "Always ensure array is sorted",
                "Watch for off-by-one errors",
                "Consider edge cases (empty array, single element)",
            ],
        ),
    }

    @classmethod
    def get_explanation(cls, algorithm_name: str) -> Optional[AlgorithmExplanation]:
        """
        Get explanation for an algorithm.

        Args:
            algorithm_name: Name of the algorithm

        Returns:
            AlgorithmExplanation or None
        """
        return cls.EXPLANATIONS.get(algorithm_name)

    @classmethod
    def list_algorithms(cls) -> List[str]:
        """
        List all algorithms with explanations.

        Returns:
            List of algorithm names
        """
        return list(cls.EXPLANATIONS.keys())

    @classmethod
    def print_explanation(cls, algorithm_name: str) -> None:
        """
        Print formatted explanation for an algorithm.

        Args:
            algorithm_name: Name of the algorithm
        """
        explanation = cls.get_explanation(algorithm_name)
        if not explanation:
            print(f"No explanation available for {algorithm_name}")
            return

        print(f"\n{'='*70}")
        print(f"Algorithm: {explanation.name}")
        print(f"{'='*70}")
        print(f"\nOverview:")
        print(f"  {explanation.overview}")
        print(f"\nHow it works:")
        print(f"  {explanation.how_it_works}")
        print(f"\nKey Concepts:")
        for concept in explanation.key_concepts:
            print(f"  • {concept}")
        print(f"\nComplexity:")
        print(f"  Time: {explanation.complexity['time']}")
        print(f"  Space: {explanation.complexity['space']}")
        print(f"\nUse Cases:")
        for use_case in explanation.use_cases:
            print(f"  • {use_case}")
        print(f"\nAdvantages:")
        for advantage in explanation.advantages:
            print(f"  • {advantage}")
        print(f"\nDisadvantages:")
        for disadvantage in explanation.disadvantages:
            print(f"  • {disadvantage}")
        if explanation.tips:
            print(f"\nTips:")
            for tip in explanation.tips:
                print(f"  • {tip}")
        if explanation.common_pitfalls:
            print(f"\nCommon Pitfalls:")
            for pitfall in explanation.common_pitfalls:
                print(f"  • {pitfall}")
        print(f"\n{'='*70}\n")

