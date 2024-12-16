from dnachisel import *
from transcriptDesigner.one_to_one_revTranslate import oneToOneReverseTranslate
import warnings
from Bio import BiopythonWarning

warnings.simplefilter('ignore', BiopythonWarning)

class TranscriptDesigner:
    def __init__(self):
        self.revTranslate = None

    def initiate(self) -> None:
        """
        Initializes the codon table, the RBS chooser and the checkers.
        """

        self.revTranslate = oneToOneReverseTranslate()
        self.revTranslate.initiate()

    
    def optimize_transcript(self, dna_sequence: str, peptide: str):
        # Define the optimization problem
        problem = DnaOptimizationProblem(
            sequence=dna_sequence,
            constraints=[
                EnforceTranslation(translation=peptide),
                EnforceGCContent(mini=0.2, maxi=0.6),
                AvoidHairpins(stem_size=10, hairpin_window=30),  # Avoid hairpins in the sequence
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
                AvoidRareCodons(species="s_cerevisiae", min_frequency=0.1)
            ],
            objectives=[
                CodonOptimize(species='s_cerevisiae')  # Optimize for S. cerevisiae codon usage
            ]
        )

        # Solve the problem
        problem.resolve_constraints()
        problem.optimize()
        return problem
        
    def run(self, protein: str):

        protein += '*'
        
        simple_dna_seq = self.revTranslate.run(protein)
        optimized_transcript = self.optimize_transcript(simple_dna_seq, protein)
        
        return optimized_transcript.sequence, optimized_transcript.constraints_text_summary()
    
if __name__ == "__main__":
    # Example usage of TranscriptDesigner
    peptide = "MGLILRWKEKKQLSSKQNAQKSRKPANTSFRQQRLKAWQPILSPQSVLPL"
    
    designer = TranscriptDesigner()
    designer.initiate()

    transcript = designer.run(peptide)
    translation = translate(transcript[0])

    print(transcript[0])
    print(translation)
    print(transcript[1]) # Constraint summary (Which Constraints Did it Pass and which did fail)
       