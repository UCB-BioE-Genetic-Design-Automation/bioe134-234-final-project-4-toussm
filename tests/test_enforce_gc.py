import pytest
from dnachisel import *

@pytest.fixture
def gc_content_limits():
    """
    Fixture providing the GC content range for testing.
    """
    return 0.4, 0.6  # 40% to 60% GC content


def test_dnachisel_enforces_gc_content(gc_content_limits):
    """
    Test that DNA Chisel enforces GC content within the specified range.
    """
    # Input DNA sequence with GC content outside the range
    low_gc_sequence = "ATATATATATATATATATATA"  # Low GC content (~0%)
    high_gc_sequence = "GCGCGCGCGCGCGCGCGCGCG"  # High GC content (~100%)
    mixed_gc_sequence = "ATGCGCATGCGATATATGCGT"  # GC content in range (~50%)

    min_gc, max_gc = gc_content_limits

    # Define the DNA optimization problem for low GC content
    low_gc_problem = DnaOptimizationProblem(
        sequence=low_gc_sequence,
        constraints=[EnforceGCContent(mini=min_gc, maxi=max_gc)],
        objectives=[CodonOptimize(species='s_cerevisiae')]
    )
    low_gc_problem.resolve_constraints()
    low_gc_problem.optimize()

    # Define the DNA optimization problem for high GC content
    high_gc_problem = DnaOptimizationProblem(
        sequence=high_gc_sequence,
        constraints=[EnforceGCContent(mini=min_gc, maxi=max_gc)],
        objectives=[CodonOptimize(species='s_cerevisiae')]
    )
    high_gc_problem.resolve_constraints()
    high_gc_problem.optimize()

    # Define the DNA optimization problem for mixed GC content
    mixed_gc_problem = DnaOptimizationProblem(
        sequence=mixed_gc_sequence,
        constraints=[EnforceGCContent(mini=min_gc, maxi=max_gc)],
        objectives=[CodonOptimize(species='s_cerevisiae')]
    )
    mixed_gc_problem.resolve_constraints()
    mixed_gc_problem.optimize()

    # Helper function to calculate GC content
    def calculate_gc_content(sequence):
        gc_count = sequence.count("G") + sequence.count("C")
        return gc_count / len(sequence)

    # Check optimized sequences for low GC content
    optimized_low_gc = low_gc_problem.sequence
    low_gc_content = calculate_gc_content(optimized_low_gc)
    assert min_gc <= low_gc_content <= max_gc, f"Low GC sequence failed: GC content {low_gc_content:.2f} not in range."

    # Check optimized sequences for high GC content
    optimized_high_gc = high_gc_problem.sequence
    high_gc_content = calculate_gc_content(optimized_high_gc)
    assert min_gc <= high_gc_content <= max_gc, f"High GC sequence failed: GC content {high_gc_content:.2f} not in range."

    # Check optimized sequences for mixed GC content
    optimized_mixed_gc = mixed_gc_problem.sequence
    mixed_gc_content = calculate_gc_content(optimized_mixed_gc)
    assert min_gc <= mixed_gc_content <= max_gc, f"Mixed GC sequence failed: GC content {mixed_gc_content:.2f} not in range."

    # Print results for verification
    print(f"Low GC optimized: {optimized_low_gc} (GC content: {low_gc_content:.2f})")
    print(f"High GC optimized: {optimized_high_gc} (GC content: {high_gc_content:.2f})")
    print(f"Mixed GC optimized: {optimized_mixed_gc} (GC content: {mixed_gc_content:.2f})")
