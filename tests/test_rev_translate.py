import pytest
from transcriptDesigner.one_to_one_revTranslate import oneToOneReverseTranslate

@pytest.fixture
def reverse_translator():
    """
    Fixture to initialize and load the oneToOneReverseTranslate class.
    """
    translator = oneToOneReverseTranslate()
    translator.initiate()
    return translator


def test_reverse_translate_single_peptide(reverse_translator):
    """
    Test reverse translation for a single amino acid.
    """
    peptide = "M"  # Methionine
    dna_seq = reverse_translator.run(peptide)

    assert dna_seq == reverse_translator.amino_acid_to_codon["M"], (
        f"Expected {reverse_translator.amino_acid_to_codon['M']} for 'M', but got {dna_seq}."
    )


def test_reverse_translate_short_peptide(reverse_translator):
    """
    Test reverse translation for a short peptide sequence.
    """
    peptide = "MAG"  # Methionine, Alanine, Glycine
    dna_seq = reverse_translator.run(peptide)

    expected_seq = (
        reverse_translator.amino_acid_to_codon["M"]
        + reverse_translator.amino_acid_to_codon["A"]
        + reverse_translator.amino_acid_to_codon["G"]
    )
    assert dna_seq == expected_seq, f"Expected {expected_seq}, but got {dna_seq}."


def test_reverse_translate_long_peptide(reverse_translator):
    """
    Test reverse translation for a long peptide sequence.
    """
    peptide = "MGLILRWKEKKQLSSKQNAQKSRKPANTSFRQQRLKAWQPILSPQSVLPL"
    dna_seq = reverse_translator.run(peptide)

    expected_seq = "".join([reverse_translator.amino_acid_to_codon[aa] for aa in peptide])
    assert dna_seq == expected_seq, f"Expected {expected_seq}, but got {dna_seq}."


def test_reverse_translate_invalid_amino_acid(reverse_translator):
    """
    Test reverse translation with an invalid amino acid.
    """
    peptide = "MZ"  # 'Z' is not a standard amino acid

    with pytest.raises(KeyError):
        reverse_translator.run(peptide)


def test_reverse_translate_empty_peptide(reverse_translator):
    """
    Test reverse translation with an empty peptide string.
    """
    peptide = ""
    dna_seq = reverse_translator.run(peptide)

    assert dna_seq == "", "Expected an empty DNA sequence for an empty peptide."


def test_amino_acid_to_codon_mapping(reverse_translator):
    """
    Test if the amino_acid_to_codon dictionary is properly loaded.
    """
    assert "M" in reverse_translator.amino_acid_to_codon, "'M' (Methionine) should be in the codon dictionary."
    assert "A" in reverse_translator.amino_acid_to_codon, "'A' (Alanine) should be in the codon dictionary."
    assert isinstance(reverse_translator.amino_acid_to_codon["M"], str), "Codon for 'M' should be a string."
