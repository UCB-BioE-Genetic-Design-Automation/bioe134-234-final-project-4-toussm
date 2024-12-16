from collections import Counter  # Import Counter for counting codons
import csv
import os

class CodonChecker:
    """
    Description: 
    This class checks codon usage for a given CDS and calculates metrics like:
    1. Codon Diversity: Fraction of unique codons.
    2. Rare Codon Count: Number of rare codons in the sequence.
    3. Codon Adaptation Index (CAI): Based on codon usage frequencies.

    Input (run method):
    cds (List[str]): A list of codons representing the coding sequence (e.g., ['ATG', 'TAA', 'CGT']).

    Output:
    Tuple[bool, float, int, float]: A tuple containing:
        - codons_above_board (bool): True if the CDS passes the thresholds, False otherwise.
        - codon_diversity (float): Fraction of unique codons.
        - rare_codon_count (int): Number of rare codons.
        - cai_value (float): CAI value.
    """

    codon_frequencies: dict[str, float]

    def initiate(self) -> None:
        """
        Loads codon usage data from a file and sets up the codon frequencies and rare codons.
        """
        codon_usage_file = 'transcriptDesigner/data/yeast_codon_usage_table.tsv'
        self.codon_frequencies = {}


        # Open and read the TSV file
        with open(codon_usage_file, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')

            for row in reader:
                codon = row['Codon']
                amino_acid = row['Amino Acid']
                frequency = float(row['Frequency'])

                # Skip rows with missing codons or amino acids
                if not codon or not amino_acid:
                    continue

                self.codon_frequencies[codon] = frequency


    def run(self, cds: str) -> tuple[bool, float, float]:
        """
        Calculates codon diversity, rare codon count, and Codon Adaptation Index (CAI) for the provided CDS.
        Returns a boolean indicating whether the codons pass specified thresholds.

        :param cds: List of codons representing the CDS.
        :return: Tuple containing a boolean, codon diversity, rare codon count, and CAI score.
        """
        if not cds:
            return False, 0.0, 0, 0.0  # Return false for empty CDS

        # Calculate codon diversity
        codons = [cds[i:i+3] for i in range(0, len(cds), 3)]
        codon_counts = Counter(codons)
        codon_diversity = len(codon_counts) / 61


        # Calculate CAI (Codon Adaptation Index) as the geometric mean of codon frequencies
        cai_numerators = [self.codon_frequencies.get(codon, 0.01) for codon in codons]  # Use 0.01 for unknown codons
        cai_product = 1
        for freq in cai_numerators:
            cai_product *= freq
        
        cai_value = cai_product ** (1 / len(cai_numerators)) #if cai_numerators else 0.0

        # Apply thresholds to determine if the codons are above board
        diversity_threshold = 0.3
        cai_threshold = 0.2

        codons_above_board = (codon_diversity >= diversity_threshold and
                              cai_value >= cai_threshold)

        return codons_above_board, codon_diversity, cai_value