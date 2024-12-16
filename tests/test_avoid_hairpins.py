import pytest
from dnachisel import *

@pytest.fixture
def hairpin_test_case():
    """
    Fixture to provide a test case for AvoidHairpins.
    """
    return {
        "dna_sequence": "ATGCGTACGTTGACCTGATCCGAGTACTGATCGTAGCGCGCTCGAGCTCGAGCGTATCGTAGCGTAGCGCTAGCGCGTAGCTCGAGA",
        "expected_hairpins": [
            (10, 50),  # Example of a hairpin loop location
            (30, 70)
        ]
    }

def test_dnachisel_avoid_hairpins(hairpin_test_case):
    """
    Test that DNA Chisel removes hairpins from the DNA sequence.
    """
    dna_sequence = hairpin_test_case["dna_sequence"]
    min_stem_size = 10
    hairpin_window = 30
    peptide = translate(dna_sequence)

    # Define the DNA optimization problem
    problem = DnaOptimizationProblem(
        sequence=dna_sequence,
        constraints=[
            AvoidHairpins(stem_size=min_stem_size, hairpin_window=hairpin_window),
            EnforceTranslation(translation=peptide)
        ],
        objectives=[
            CodonOptimize(species='s_cerevisiae')
        ]
    )

    # Solve the optimization problem
    problem.resolve_constraints()
    problem.optimize()

    # Check if all constraints pass
    assert problem.all_constraints_pass(), "Hairpins detected in the optimized sequence."

    # Print results for debugging
    optimized_sequence = problem.sequence
    print(f"Original DNA: {dna_sequence}")
    print(f"Optimized DNA: {optimized_sequence}")
