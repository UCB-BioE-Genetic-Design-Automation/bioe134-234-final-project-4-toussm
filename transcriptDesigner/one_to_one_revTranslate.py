import csv
import os

class oneToOneReverseTranslate:
    '''
    Does a simple one amino acid to one codon mapping of a peptide.
    '''
    amino_acid_to_codon: dict[str: str]

    def initiate(self) -> None:
        codon_dict = {}
        file_path = "transcriptDesigner/data/yeast_codon_usage_table.tsv"

        # Open and read the TSV file
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')

            for row in reader:
                codon = row['Codon']
                amino_acid = row['Amino Acid']
                frequency = float(row['Frequency'])

                # Skip rows with missing codons or amino acids
                if not codon or not amino_acid:
                    continue

                # Check if this codon has the highest frequency for the amino acid
                if amino_acid not in codon_dict or frequency > codon_dict[amino_acid]['Frequency']:
                    codon_dict[amino_acid] = {'Codon': codon, 'Frequency': frequency}

        # Convert the dictionary to a simple mapping of amino acid to codon
        self.amino_acid_to_codon = {aa: data['Codon'] for aa, data in codon_dict.items()}

    def run(self, peptide: str) -> str:
        dna_seq = ""
        for aa in peptide:
            dna_seq += self.amino_acid_to_codon[aa]

        return dna_seq
    
if __name__ == "__main__":
    # Example usage of oneToOneReverseTranslate
    peptide = "MGLILRWKEKKQLSSKQNAQKSRKPANTSFRQQRLKAWQPILSPQSVLPL"
    
    simple_rev_translate = oneToOneReverseTranslate()
    simple_rev_translate.initiate()

    revTranslation = simple_rev_translate.run(peptide)

    print(revTranslation)
    