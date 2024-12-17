# oneToOneReverseTranslate

## Overview

The **`oneToOneReverseTranslate`** class is a simple yet essential helper class for the **`cdsDesigner`** project. It performs a straightforward reverse translation of a protein sequence into a DNA sequence by mapping each amino acid to its most frequent codon. This implementation serves as a foundation for generating initial coding sequences (CDS) that can later be optimized for yeast-specific constraints.

While the implementation was straightforward, the **`oneToOneReverseTranslate`** class proved to be an invaluable tool for the **`cdsDesigner`**. It allowed the pipeline to:
1. Quickly generate DNA sequences from protein sequences.
2. Ensure consistent codon usage before further optimization.

---

## Class Functionality

The **`oneToOneReverseTranslate`** class:
1. **Loads the Codon Table**: Reads the codon usage table for yeast (*Saccharomyces cerevisiae*) from a TSV file.
2. **Maps Amino Acids to Codons**: For each amino acid, it selects the codon with the **highest frequency** in yeast.
3. **Reverse Translates a Protein Sequence**: Converts a protein sequence into its corresponding DNA sequence using the one-to-one mapping.

---

## Code Components

### **1. Codon Table Initialization**
The **`initiate`** method loads the yeast codon usage table from a TSV file and maps each amino acid to its most frequent codon.

### **2. Reverse Translation**
The run method takes a protein sequence as input and reverse-translates it into a DNA sequence using the amino acid-to-codon mapping. It will raise a `ValueError` if an invalid sequence is input (it has a non-amino acid or there are lower case).

## Conclusion
The oneToOneReverseTranslate class is a critical helper tool for generating DNA sequences from protein sequences in a biologically relevant manner. Its simple yet effective implementation ensures that the downstream optimization pipeline starts with a clean and consistent input.