# Structural Constraints in Natural Language: An Empirical Study of Dependency Trees

## Overview

This project investigates whether the structure of natural language dependency trees is random or governed by systematic constraints.

We compare real dependency trees from multiple languages with uniformly random trees of the same size to understand how natural language organizes syntax.

---

## Core Insight

Natural language dependency trees are **not random**.

They exhibit consistent structural patterns characterized by:

- **Minimization of dependency length**
- **Reduced structural complexity along paths**
- **More compact and locally organized hierarchies**

These results suggest that language is optimized not just linearly, but also **structurally**.

---

## Key Findings

### 1. Dependency Length Minimization (Baseline)
- Natural trees have **significantly lower dependency length**
- Random trees exceed real trees in **~95–99% of cases**

➡️ Strong pressure to keep related words close

---

### 2. Intervener Complexity (IC / WIC)
- Natural trees have **fewer intervening heads between dependencies**
- Weighted version (WIC) shows even stronger separation

➡️ Dependencies avoid structurally complex regions

---

### 3. Path Integration Cost (PIC) — **Strongest Result**
- Measures structural load along paths between all node pairs
- Natural trees have **substantially lower PIC than random trees**

➡️ Language minimizes **global structural processing cost**, not just linear distance

---

### 4. Hierarchical Locality (LCA Depth)
- Natural trees tend to have **deeper LCAs**
- Indicates stronger **local grouping of related words**

➡️ Syntax is organized into tighter structural clusters

---

### 5. Shallower but More Organized Structures
- Natural trees are generally **less deep**
- But not simply flatter — they are **structured efficiently**

---

### 6. Cross-Linguistic Consistency
- Observed across multiple typologically diverse languages
- Suggests **universal structural constraints**

---

### 7. Statistical Validation
- Differences are **highly significant (p < 0.001)** across metrics
- Confirms patterns are not due to randomness

---

## Methodology

### Data
- **SUD (Surface Universal Dependencies) corpus**
- Multiple languages with diverse syntactic properties

### Pipeline
For each sentence of length *n*:
1. Extract real dependency tree
2. Generate **20 random trees** (uniform via Prüfer sequences)
3. Compute structural metrics
4. Compare real vs random distributions

---

## Metrics

### Core Metrics

- **Dependency Length (DL)**  
  Linear distance between head and dependent

- **Intervener Complexity (IC)**  
  Number of intervening heads between dependency endpoints

- **Weighted IC (WIC)**  
  IC weighted by outdegree of intervening nodes

- **Path Integration Cost (PIC)**  
  Global structural cost over all node pairs  
  *(computed in O(n) using subtree decomposition)*

- **Average LCA Depth**  
  Depth at which pairs of nodes merge in the tree

---

### Structural Metrics

- **Tree Depth**  
  Maximum root-to-leaf distance

- **Average Depth**  
  Mean node depth

- **Maximum Arity**  
  Maximum branching factor

- **Degree Entropy** *(auxiliary)*  
  Variability in branching

---

## Algorithmic Contributions

Several metrics are naively **O(n²)** but are optimized to **O(n)**:

- PIC → computed via **node contribution decomposition**
- LCA-based metric → computed via **subtree aggregation**
- IC/WIC → optimized using **prefix sums**

➡️ Avoids pairwise enumeration and enables large-scale experiments

---

## Project Structure

```
src/
  tree_gen.py        # Random tree generation (Prüfer)
  dep_tree.py        # Dependency tree construction
  metrics.py         # Structural metrics (optimized)

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

All outputs are saved in the `results/` directory.

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
  - word order constraints

Future work:
- structured random baselines
- projective tree constraints
- typology-aware models

---

## Conclusion

Natural language is **not a random system**.

It systematically:
- minimizes dependency length  
- reduces structural interference (IC/WIC)  
- minimizes global structural cost (PIC)  

These results indicate that language is shaped by both:
- **linear efficiency**
- **hierarchical processing constraints**

---

## Author

**Pujit Sharath Shetty**
