import pytest
from dnachisel import *
from cdsDesigner.one_to_one_revTranslate import oneToOneReverseTranslate

@pytest.fixture
def translation_test_case():
    """
    Fixture to provide a test case for EnforceTranslation.
    """
    revTranslate = oneToOneReverseTranslate()
    revTranslate.initiate()
    peptide = "MRFWYVGKPTALNQHIDCEYAGLSTVWPQK"
    dnaseq = revTranslate.run(peptide)
    return {
        "dna_sequence": dnaseq,
        "protein_sequence": peptide,
    }

def test_dnachisel_enforce_translation(translation_test_case):
    """
    Test that DNA Chisel enforces the correct translation of a DNA sequence.
    """
    dna_sequence = translation_test_case["dna_sequence"]
    protein_sequence = translation_test_case["protein_sequence"]

    # Define the DNA optimization problem
    problem = DnaOptimizationProblem(
        sequence=dna_sequence,
        constraints=[
            EnforceTranslation(translation=protein_sequence),  # Ensure correct translation
            AvoidPattern("GAATTC")  # Example: Avoid EcoRI site
        ],
        objectives=[CodonOptimize(species='s_cerevisiae')]
    )

    # Solve the optimization problem
    problem.resolve_constraints()
    problem.optimize()

    # Verify that all constraints pass
    assert problem.all_constraints_pass(), "Some constraints were not satisfied."

    # Translate the optimized sequence to protein and validate
    optimized_sequence = problem.sequence
    translated_protein = translate(optimized_sequence)
    assert translated_protein == protein_sequence, (
        f"Translation mismatch: expected '{protein_sequence}', got '{translated_protein}'."
    )

    # Print results for debugging
    print(f"Original DNA: {dna_sequence}")
    print(f"Optimized DNA: {optimized_sequence}")
    print(f"Translated Protein: {translated_protein}")
