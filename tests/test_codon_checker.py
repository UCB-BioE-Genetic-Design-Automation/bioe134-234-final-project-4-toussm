import pytest
from checkers.codon_checker import CodonChecker  # Update this import path as necessary

@pytest.fixture
def codon_checker():
    """
    Fixture to initialize and load the CodonChecker with codon usage frequencies.
    """
    checker = CodonChecker()
    checker.initiate()
    return checker


def test_codon_checker_valid_cds(codon_checker):
    """
    Test the CodonChecker with a valid CDS that meets the diversity and CAI thresholds.
    """
    valid_cds = "ATGGCTGCCGTTTTTCAATGGAGCGTACGACCTGTGCTACTGGCATTCCGACATGCGCTACGTTGGTCTGACTAAGTAG"  # A hypothetical CDS
    codons_above_board, codon_diversity, cai_value = codon_checker.run(valid_cds)

    print(f"Codons Above Board: {codons_above_board}")
    print(f"Codon Diversity: {codon_diversity:.2f}")
    print(f"CAI Value: {cai_value:.2f}")

    assert codons_above_board, "Codons should meet the thresholds for a valid CDS."
    assert codon_diversity >= 0.3, "Codon diversity should meet the threshold."
    assert cai_value >= 0.2, "CAI value should meet the threshold."


def test_codon_checker_invalid_cds_low_diversity(codon_checker):
    """
    Test the CodonChecker with a CDS that has low codon diversity.
    """
    low_diversity_cds = "ATGATGATGATGATGATGATGTAA"  # Repetitive codons, low diversity
    codons_above_board, codon_diversity, cai_value = codon_checker.run(low_diversity_cds)

    print(f"Codons Above Board: {codons_above_board}")
    print(f"Codon Diversity: {codon_diversity:.2f}")
    print(f"CAI Value: {cai_value:.2f}")

    assert not codons_above_board, "Codons should fail the diversity threshold."
    assert codon_diversity < 0.3, "Codon diversity should be below the threshold."


def test_codon_checker_invalid_cds_low_cai(codon_checker):
    """
    Test the CodonChecker with a CDS that has low CAI.
    """
    low_cai_cds = "GTACGTACGTTTTTTTTTGGATGCGTAGTAGTACTCCTCCTCCTCCTCCTCCTC"  # Rare codons included, low CAI
    codons_above_board, codon_diversity, cai_value = codon_checker.run(low_cai_cds)

    print(f"Codons Above Board: {codons_above_board}")
    print(f"Codon Diversity: {codon_diversity:.2f}")
    print(f"CAI Value: {cai_value:.2f}")

    assert not codons_above_board, "Codons should fail the CAI threshold."
    assert cai_value < 0.2, "CAI value should be below the threshold."


def test_codon_checker_empty_cds(codon_checker):
    """
    Test the CodonChecker with an empty CDS.
    """
    empty_cds = ""
    codons_above_board, codon_diversity, cai_value = codon_checker.run(empty_cds)

    assert not codons_above_board, "Empty CDS should fail."
    assert codon_diversity == 0.0, "Codon diversity should be 0 for an empty CDS."
    assert cai_value == 0.0, "CAI value should be 0 for an empty CDS."
