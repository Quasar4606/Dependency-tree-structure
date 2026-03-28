# Empirical Properties of Dependency Trees in Natural Languages

## Overview
This project investigates the structural properties of dependency trees in natural languages and compares them with randomly generated trees of the same size.

The goal is to determine whether natural language syntax exhibits systematic structural constraints or resembles random tree structures.

---

## Key Findings
- Natural language trees are **shallower** than random trees  
- Natural language exhibits **higher branching (maximum node arity)**  
- Random trees are deeper in the majority of cases across all languages  
- These patterns are **consistent across multiple languages**  
- Differences are **statistically significant (p < 0.001)**  

---

## Methodology
- Dependency trees are extracted from the **SUD (Surface Universal Dependencies) corpus**
- Each sentence is represented as a directed tree (parent → children)
- For each sentence of length *n*:
  - The real dependency tree is analyzed
  - **20 random trees** of size *n* are generated using the **Prüfer sequence method**
- Metrics computed:
  - Tree depth (longest root-to-leaf path)
  - Maximum node arity (maximum number of children)

---

## Project Structure
```
src/        # Core modules (tree generation, parsing, metrics)
scripts/    # Experiment and analysis scripts
results/    # Generated CSV files and plots
```

---

## Reproducibility

To run the full experiment:

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
```

This will:
- Process dependency treebanks
- Generate random trees
- Compute structural metrics
- Save results in the `results/` directory

---

## Languages Used
- English
- French
- German
- Spanish
- Italian
- Russian
- Chinese
- Arabic
- Hindi
- Japanese

---

## Author
Pujit Sharath Shetty
