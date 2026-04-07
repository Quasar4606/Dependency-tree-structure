# Structural Constraints in Natural Language: An Empirical Study of Dependency Trees

## Overview

This project investigates whether the structure of natural language dependency trees is random or governed by systematic constraints.

We compare real dependency trees from multiple languages with uniformly random trees of the same size to understand how natural language organizes syntax.

---

## Core Insight

Natural language dependency trees are **not random**.  
They exhibit a consistent structural pattern characterized by:

- **Reduced depth** (shallower hierarchies)
- **Increased branching** (higher local connectivity)
- **Strong minimization of dependency length**

These properties suggest that natural language is optimized to balance **efficiency, expressiveness, and cognitive constraints**.

---

## Key Findings

### 1. Dependency Length Minimization (Strongest Result)
- Natural trees have **significantly lower dependency length** than random trees
- Random trees show higher dependency length in **95–99% of sentences**
- This pattern is **consistent across all languages**

➡️ Indicates strong pressure to keep related words close

---

### 2. Shallower Structures
- Natural trees are consistently **less deep** than random trees
- Random trees are deeper in **70–90% of cases**

➡️ Deep hierarchical chains are systematically avoided

---

### 3. Increased Branching (Flatter Trees)
- Natural trees exhibit **higher maximum arity**
- Structure favors **wide, shallow organization**

➡️ Supports efficient information distribution

---

### 4. Cross-Linguistic Consistency
- Observed across **10 typologically diverse languages**
- Suggests **universal structural constraints**

---

### 5. Depth Scaling Behavior (Advanced Analysis)
- Depth grows more slowly with sentence length in natural trees
- Indicates **controlled hierarchical growth**

---

### 6. Statistical Validation
- All primary differences are **highly significant (p < 0.001)**
- Confirms results are not due to random variation

---

## Methodology

### Data
- **SUD (Surface Universal Dependencies) corpus**
- 10 languages with diverse syntactic structures

### Pipeline
For each sentence of length *n*:
1. Extract real dependency tree
2. Generate **20 random trees** using Prüfer sequences
3. Compute structural metrics
4. Compare real vs random distributions

---

## Metrics

- **Tree Depth**  
  Longest root-to-leaf path (hierarchical complexity)

- **Average Depth**  
  Mean distance of nodes from root (global structure)

- **Maximum Arity**  
  Maximum number of children of any node (branching factor)

- **Dependency Length**  
  Distance between syntactically related words (efficiency)

- **Degree Entropy** *(auxiliary)*  
  Variability of branching structure

---

## Project Structure

```
src/
  tree_gen.py        # Random tree generation (Prüfer)
  dep_tree.py        # Dependency tree construction
  metrics.py         # Structural metrics

scripts/
  run_pipeline.py            # Main experiment pipeline
  plot_results.py           # Per-language plots
  cross_language_table.py   # Summary table
  cross_language_plot.py    # Cross-language visualizations
  stats_test.py             # Statistical tests
  depth_scaling.py          # Scaling analysis

results/
  language/         # Per-language outputs
  cross_language/   # Global summaries and plots
```

---

## Reproducibility

### Setup

```
pip install -r requirements.txt
```

### Run full experiment

```
python scripts/run_pipeline.py
python scripts/plot_results.py
python scripts/cross_language_table.py
python scripts/cross_language_plot.py
python scripts/stats_test.py
python scripts/depth_scaling.py
```

All outputs will be saved in the `results/` directory.

---

## Languages

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

## Limitations

- Random trees are **uniform and unconstrained**
- They do not enforce:
  - projectivity
  - linguistic degree distributions

Future work could use more linguistically informed baselines.

---

## Conclusion

Natural language is **not a random system**.

It exhibits structured patterns that:
- minimize dependency length  
- limit hierarchical depth  
- increase branching  

Together, these properties indicate that language is shaped by **efficiency and cognitive constraints**, rather than arbitrary structure.

---

## Author

**Pujit Sharath Shetty**
