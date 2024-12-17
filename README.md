
# BioE 134 Final Project Submission

## Project Overview

This project aims to design an optimized plasmid prototype to be transformed into S. cerevisiae to express the protein of choice. The project has 6 major components: 

1. **Input protein name**: Retrieves an amino acid sequence for the gene in S. cerevisiae from UniProt that the user has input.
2. **Design and Optimize CDS**: Takes the amino acid sequence as input and optmizes a CDS accordingly as well as providing an optmization report.
3. **Design UTRs and Promoters**: Takes the optimized CDS and outputs optimal 5' and 3' UTRs and a promoter to enable expression.
4. **Translate to Construction File**: Takes the optimized CDS, designed UTRs, and promoter to create a wet lab protocol formatted in a construction file. The protocol will be defined by the user and the file is generated accordingly.
5. **Validate Construction File**: This uses a construction file simulator to simulate the construction file which describes the experiment.
6. **Wrappers**: The wrappers describe the functions and their descriptions, inputs, outputs, how to execute them, and other semantics necessary for C9 communication. The wrappers enable the LLM to communicate with C9 given a users prompt.

These functions are implemented in **Python** and are part of the broader bioinformatics toolset aimed at automating genetic sequence analysis tasks.

---

## Scope of Work

As part of the final project for BioE 134, I developed two classes as well as complementary validation scripts that are foundational for optimizing the design of a plasmid prototype for S. cerevisiae:

1. **Class: cdsDesigner**: This class generates an optimized CDS corresponding to a given protein sequence. It provides an optimization summary and codon usage statistics as well.
   
2. **one_to_one_revTranslate**: This performs a simple one-to-one reverse translation of a protein sequence into a DNA sequence using the most frequently used codons for each amino acid.

Both functions include input validation and error handling to ensure proper use. The cdsDesigner uses a python library called dnachisel which raises an error for invalid inputs, optimization failures, and any optmizations that failed will be captured in the report, while the reverse translate function raises an error for sequences protein sequences containing invalid characters.

---

## Class Descriptions

### 1. CDS Designer (`cdsDesigner`)

- **Description**: The class once initiated, will take a protein sequence as an argument to the run method. It utilizes the dnachisel library to codon optimize the cds for the given protein sequence.
- **Input**: A string representing the protein amino acid sequence.
- **Output**: A tuple of strings containing: optimized cds, optimization report, and codon usage statistics(codon diversity and CAI value)

**Example**:
```python
designer = cdsDesigner()
designer.initiate()
designer.run("MAGWQ")
# Returns: "ATGGCCGGGTGGCAGTAA", "===> SUCCESS - all constraints evaluations pass...", "Codon Check Passed. Codon Diversity (some float), CAI Value: (some float)"
```

### 2. Reverse Translate (`one_to_one_revTranslate`)

- **Description**: This function translates a protein sequence into a corresponding DNA sequence using the most frequent codons per amino acid for S. cerevisiae. It is a helper class for cdsDesigner.
- **Input**: A string representing the protein sequence.
- **Output**: A string representing the reverse translated DNA sequence.

**Example**:
```python
revTranslate = one_to_one_revTranslate()
revTranslate.initiate()
revTranslate.run("MGLILRWKEKKQLSSKQNAQKSRKPANTSFRQQRLKAWQPILSPQSVLPL")
# Returns: "ATGGGTTTGATTTTGAGATGGAAAGAAAAAAAACAATTGTCTTCTAAACAAAATGCTCAAAAATCTAGAAAACCAGCTAATACTTCTTTTAGACAACAAAGATTGAAAGCTTGGCAACCAATTTTGTCTCCACAATCTGTTTTGCCATTG"
```

---

## Error Handling

### cdsDesigner
- Raises errors if the `dnachisel` library finds an error. Examples are invalid inputs or it couldn't find a solution to a constraint. These are just a couple of examples, but there are more listed in its documentation.

### Reverse Translate
- Raises `ValueError` if the protein sequence contains invalid characters.

---

## Testing

Both classes have been tested with standard, edge, and invalid input cases. A comprehensive suite of tests has been implemented using **pytest**.

- **Test Files**: In `tests/` folder

The tests include:
- Testing for hairpins
- Testing for forbidden sequences and promoters
- Testing for meeting GC content requirements
- Testing for rare codons
- Testing if the translation of the optimized sequence is correct
- Testing the if a protein sequence is properly reverse translated

---

## Benchmarking

The cdsDesigner optimization performance has been benchmarked on the S.cerevisiae proteome found in `benchmarker/UP000002311_559292.fasta`. It displayed exceptional performance as it processed and optimized all 6060 genes in the proteome in just about 317 seconds and
it passed all constraints that were given to `dnachisel`. Furthermore, there is one translation failure because the gene did start with M, and only 11% of the genes did not pass the codon usage check (either failing codon diversity or CAI).
Given the large number of constraints, the optmizer was able to handle them remarkably.

What the benchmarker does:
- It processes all the genes and their amino acid sequences in the proteome
- Then it keeps track of successful results and error results (optimization errored)
- Then it validates the sequences by checking translation, sequence validity, parsing the optimization summary to see if constraints were not met, and it also checks if codon usage passes. These are all stored for the next step.
- Lastly, it goes through the validation failures to count the number of failure type occurences (i.e. "Fobidden Sequences") and it writes the summary of the validation and it writes a file that contains the validation failures for the genes that had them.
It also writes a error summary capturing any errors that occured.
- These can be found for the proteome benchmark in `summary_report.txt`, `validation_failures.tsv`, and `error_summary report`.

## Usage Instructions

Clone the repository and install the required dependencies listed in `requirements.txt`. The classes can be imported from the `cdsDesigner/cds_Designer.py` and `cdsDesigner/one_to_one_revTranslate.py` modules.

**Example**:

```bash
pip install -r requirements.txt
```

Once installed, you can use the classes as follows:

```python
from cdsDesigner.cdsDesigner import cdsDesigner
from cdsDesigner.one_to_one_revTranslate import oneToOneReverseTranslate

# Example DNA sequence
peptide = "MGLILRWKEKKQLSSKQNAQKSRKPANTSFRQQRLKAWQPILSPQSVLPL"
designer = cdsDesigner()
designer.initiate()

revTranslate = oneToOneReverseTranslate()
revTranslate.initiate()

# optimize sequence
optimized_seq = designer.run(peptide)
print(optimized_seq) # Will print the sequence, optimization report, and the codon usage report

# Reverse Translate
revTranslation = revTranslate.run(peptide)
print(revTranslation) # Will print reverse translation of peptide
```

---

## Conclusion

These two classes provide foundational operations for working with amino acid sequences in bioinformatics pipelines. They have been tested and documented, ensuring proper error handling and robust functionality.
