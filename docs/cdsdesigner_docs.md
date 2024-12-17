# Documentation of my cdsDesigner class

---

## Overview

The **`cdsDesigner`** class is a Python-based tool that designs and optimizes coding sequences (CDS) for yeast (*Saccharomyces cerevisiae*) using the **DNA Chisel** library (API Documentation: https://edinburgh-genome-foundry.github.io/DnaChisel/index.html#related-projects). The class:
1. Performs reverse translation of a protein sequence into a DNA sequence using a one-to-one codon mapping strategy.
2. Optimizes the generated CDS to meet constraints such as GC content, forbidden sequences, avoidance of hairpins, and codon diversity.
3. Ensures the resulting sequence conforms to yeast-specific biological constraints and codon usage preferences.

This tool integrates components for reverse translation, codon optimization, and validation, ensuring the sequence is suitable for expression in yeast.

---

## Class Components

### **1. Initialization and Setup**
The `__init__` and `initiate` methods prepare the class for operation:
- **`oneToOneReverseTranslate`**: Maps amino acids to the most frequent codons for yeast.
- **`CodonChecker`**: Evaluates codon diversity and Codon Adaptation Index (CAI).

**Code:**
```python
def initiate(self) -> None:
    self.revTranslate = oneToOneReverseTranslate()
    self.revTranslate.initiate()
    self.codonChecker = CodonChecker()
    self.codonChecker.initiate()
```

### **2. CDS Optimization**
The `optimize_cds` method takes a DNA sequence and a peptide as input and optimizes the sequence using DNA Chisel.

**Key Constraints:**
- **GC Content**: Between 30%–60% (typical range for yeast).
- **Hairpins**: Avoid stems of 10 bp with windows of 30 bp.
- **Forbidden Patterns**:
- Restriction enzyme sites (e.g., EcoRI, BamHI, HindIII).
- Poly-nucleotide repeats like AAAAAAA, TTTTTTTT.
- Constitutive promoter sequences to avoid unintended expression.
- **Rare Codons**: Minimize rare codons for S. cerevisiae.
**Objective:**
- **Codon Optimization**: Optimizes the DNA sequence given yeast codon usage preferences. It is essentially solving a multi-optimization problem to solve all the constraints. It outputs the best solution. Any failed constraints are recorded in the optimization summary.
If it can't find a solution it will throw an error, but I beleive it still outputs a sequence (I could be wrong). Also there may be other errors that it throws that I have not come across.

### **3. Execution and Codon Validation**
The run method:

1. Ensures the input protein sequence ends with a stop codon (*).
2. Generates a simple reverse-translated sequence.
3. Optimizes the sequence using the optimize_cds method.
4. Runs the CodonChecker to validate codon diversity and CAI.
**Output:**

- Optimized DNA sequence.
- Constraint optimization summary.
- Codon check results: Diversity score and CAI value.

## Key Challenges and Learnings
### **1. Understanding DNA Chisel**
Initially, I struggled with understanding how to use the DNA Chisel library effectively. It took a lot of time to read through a surprisingly sparse documentation and understand how to set up my code. Specifically:

- **Constraints:** Identifying the correct constraints to optimize CDS sequences for yeast.
- **Objectives:** Learning how to balance constraints (e.g., GC content, avoiding forbidden patterns) with codon optimization.
**Solution:** I explored the documentation and performed trial-and-error with different constraints to see their impact.

### **2. Biological Context for Yeast Optimization**
Designing a CDS for yeast required understanding:

**Forbidden Sequences:**
- Restriction sites (EcoRI, BamHI).
- Poly-nucleotide repeats that could cause sequencing errors.
- Intron splice sites
- Constitutive promoter sequences to avoid unintentional gene activation.
**GC Content:** Yeast has an average GC content of ~38%, so I targeted a range of 30%–60%.
**Hairpin Avoidance:** Typical yeast RNA structures have stems of ~10 bp, so I enforced a hairpin size limit.

### **3. Codon Diversity and Rare Codons**
I had to determine:

- What level of codon diversity is acceptable?
→ 0.3–0.4 diversity was sufficient for yeast.
- How to minimize rare codons while maintaining CAI > 0.2.
This involved using `AvoidRareCodons` and validating with my custom `CodonChecker`.

### **4. Debugging Complex Errors**
Debugging errors while integrating DNA Chisel was challenging because:

- Library errors were sometimes hard to trace and hard to debug.
- Circular imports or module path issues caused confusion.
**Solution:**

- I learned to isolate and test components individually.
- Used print statements and step-through debugging to pinpoint issues.

## **Conclusion**
Through this project, I learned:

1. How to use DNA Chisel for sequence optimization.
2. Biological constraints for yeast CDS design.
3. Debugging and resolving errors when integrating complex libraries.