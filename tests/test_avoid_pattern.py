import pytest
from dnachisel import *

@pytest.fixture
def forbidden_patterns():
    """
    Fixture providing the list of forbidden patterns for testing.
    """
    return [
        "GAATTC",  # EcoRI restriction site
        "GGATCC",  # BamHI restriction site
        "AAAAAAA",  # poly(A)
        "TATAAA",  # TATA box
        "AAGCTT",  # HindIII restriction site
        "GCGGCCGC",  # NotI restriction site
        "GTAAGT",  # intron splice sites
        "GTGAGT",  # intron splice sites
        "TTTTTTTT",  # poly(T)
        "CCCCCCCC",  # poly(C)
        "GGGGGGGG",  # poly(G)
        "ATATATAT",  # poly(AT)
        "CAATTG",  # MfeI
        "AGATCT",  # BglII
        "ACTAGT",  # SpeI
        "TCTAGA",  # XbaI
        "GGTCTC",  # BsaI
        "CGTCTC",  # BsmBI
        "CACCTGC",  # AarI
        "CTGCAG",  # PstI
        "CTCGAG",  # XhoI
    ]


def test_dnachisel_avoids_all_patterns(forbidden_patterns):
    """
    Test that DNA Chisel avoids all specified forbidden patterns in the optimized sequence.
    """
    # Input DNA sequence containing multiple forbidden patterns
    dna_sequence = "ATGGCCATTGAATTCCATGGGCCGCTGGATCCTGAAAGGGTGCCCGTATAAAAAGCTTGCGGCCGCGTAAGTGTGAGTTTTTTTTCCCCCCCCGGGGGGGGATATATATCAATTGAGATCTACTAGTTCTAGAGGTCTCCGTCTCCACCTGCCTGCAGCTCGAGAAAA"

    peptide = translate(dna_sequence)

    # Define the DNA optimization problem
    problem = DnaOptimizationProblem(
        sequence=dna_sequence,
        constraints=[EnforceTranslation(translation=peptide),
                    AvoidPattern("GAATTC"),  # Avoid EcoRI restriction site
                    AvoidPattern("GGATCC"),  # Avoid BamHI restriction site
                    AvoidPattern("AAAAAAA"),  # Avoid poly(A)
                    AvoidPattern("TATAAA"),  # Avoid TATA box
                    AvoidPattern("AAGCTT"),  # Avoid HindIII restriction site
                    AvoidPattern("GCGGCCGC"), # Avoid NotI restriction site
                    AvoidPattern("GTAAGT"), # Avoid intron splice sites
                    AvoidPattern("GTGAGT"), # Avoid intron splice sites
                    AvoidPattern("TTTTTTTT"),  # poly(T)
                    AvoidPattern("CCCCCCCC"),  # poly(C)
                    AvoidPattern("GGGGGGGG"),  # poly(G)
                    AvoidPattern("ATATATAT"),  # poly(AT)
                    AvoidPattern("CAATTG"),    # MfeI
                    AvoidPattern("AGATCT"),    # BglII
                    AvoidPattern("ACTAGT"),    # SpeI
                    AvoidPattern("TCTAGA"),    # XbaI
                    AvoidPattern("GGTCTC"),    # BsaI
                    AvoidPattern("CGTCTC"),    # BsmBI
                    AvoidPattern("CACCTGC"),   # AarI
                    AvoidPattern("CTGCAG"),    # PstI
                    AvoidPattern("CTCGAG"),    # XhoI
                     ],
        objectives=[
                CodonOptimize(species='s_cerevisiae')  # Optimize for S. cerevisiae codon usage
            ]

    )

    # Solve the optimization problem
    problem.resolve_constraints()
    problem.optimize()

    # Check that all forbidden patterns are absent in the optimized sequence
    for pattern in forbidden_patterns:
        assert pattern not in problem.sequence, f"Forbidden pattern {pattern} found in optimized sequence."
