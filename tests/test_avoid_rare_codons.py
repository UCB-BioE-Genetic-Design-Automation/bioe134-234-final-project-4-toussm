import pytest
from dnachisel import *

@pytest.fixture
def rare_codons_test_case():
    """
    Fixture to provide a test case for AvoidRareCodons.
    """
    return {
        "dna_sequence": (
            "ATGCGTACGTTGACCCGGCCCTGGGTTGAGATCGTAAATTCGATGGTCCCTGAGTAG"  # Contains rare codons
        ),
        "species": "s_cerevisiae",  # Target species
        "min_frequency": 0.1  # Codons with usage <10% are considered rare
    }

def test_dnachisel_avoid_rare_codons(rare_codons_test_case):
    """
    Test that DNA Chisel removes rare codons from the DNA sequence.
    """
    dna_sequence = rare_codons_test_case["dna_sequence"]
    species = rare_codons_test_case["species"]
    min_frequency = rare_codons_test_case["min_frequency"]
    peptide = translate(dna_sequence)

    # Define the DNA optimization problem
    problem = DnaOptimizationProblem(
        sequence=dna_sequence,
        constraints=[
            AvoidRareCodons(species=species, min_frequency=min_frequency),
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
    assert problem.all_constraints_pass(), "Rare codons were detected in the optimized sequence."

    # Print results for debugging
    optimized_sequence = problem.sequence
    print(f"Original DNA: {dna_sequence}")
    print(f"Optimized DNA: {optimized_sequence}")
