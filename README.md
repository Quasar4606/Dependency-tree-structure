# Structural Constraints in Natural Language: An Empirical Study of Dependency Trees

## Overview

This project investigates whether the structure of natural language dependency trees is random or governed by systematic constraints.

We compare real dependency trees from multiple languages with uniformly random trees of the same size to understand how natural language organizes syntax. By analyzing structural differences across a large dataset, we aim to identify whether language exhibits consistent, non-random patterns.

---

## Core Insight

Natural language dependency trees are **not random**.

They exhibit consistent structural patterns shaped by constraints such as:

- minimizing dependency distance
- reducing structural interference
- organizing hierarchy efficiently

These constraints operate both **locally (between words)** and **globally (across the entire tree)**.

---

## Key Findings

### 1. Dependency Length Minimization (DL)

- Natural trees have **significantly lower dependency length**
- Random trees exceed real trees in **~95–99% of sentences**

➡️ Strong and near-universal pressure to keep related words close

---

### 2. Intervener Complexity (IC / WIC)

- Natural trees have **fewer intervening heads**
- Weighted IC (WIC) shows an even stronger effect

➡️ Dependencies avoid crossing structurally dense regions

---

### 3. Path Integration Cost (PIC)

- Measures structural load across paths between all node pairs  
- Unlike DL/IC, PIC does **not show uniform dominance**

➡️ Natural language is **not simply minimizing global path cost**,  
but balancing multiple competing constraints

---

### 4. Hierarchical Organization (LCA Depth)

- Natural trees tend to have **shallower average LCA depth**
- Indicates that dependencies connect higher in the tree

➡️ Suggests more efficient hierarchical grouping

---

### 5. Depth vs Branching Tradeoff

- Natural trees are **shallower**
- But have **higher branching (arity)**

➡️ Language prefers flatter but structured trees

---

### 6. Degree Distribution

- Natural trees show slightly higher entropy
- Indicates more variability in branching

---

### 7. Cross-Linguistic Consistency

Observed across 10 languages:
English, French, German, Spanish, Italian, Russian, Chinese, Arabic, Hindi, Japanese  

➡️ Strong effects (DL, IC, WIC) are highly consistent  
➡️ Some metrics (PIC, scaling) vary across languages  

---

### 8. Statistical Validation

- Differences are **highly significant (p < 0.001)**
- Verified using:
  - paired t-tests  
  - Mann–Whitney U tests  

---

## Methodology

### Data

- Surface-Syntactic Universal Dependencies (SUD)  
- ~165,000 sentences  
- 10 languages  

---

### Pipeline

For each sentence of length *n*:

1. Extract real dependency tree  
2. Generate 20 random trees (Prüfer sequences)  
3. Convert to rooted directed trees  
4. Compute structural metrics  
5. Compare real vs random  

---

### Metrics

#### Efficiency Metrics
- Dependency Length (DL)  
- Intervener Complexity (IC)  
- Weighted IC (WIC)  

#### Global Metrics
- Path Integration Cost (PIC)  
- Average LCA Depth  

#### Structural Metrics
- Tree Depth  
- Average Depth  
- Maximum Arity  
- Degree Entropy  

---

## Algorithmic Contributions

Optimized several metrics from O(n²) → O(n):

- PIC via node contributions  
- LCA via subtree aggregation  
- IC/WIC via prefix sums  

---

## Project Structure

src/  
  tree_gen.py  
  dep_tree.py  
  metrics.py  

scripts/  
  run_pipeline.py  
  plot_results.py  
  cross_language_table.py  
  cross_language_plot.py  
  stats_test.py  
  depth_scaling.py  

results/  
  language/  
  cross_language/  

---

## Reproducibility

pip install -r requirements.txt  

python scripts/run_pipeline.py  
python scripts/plot_results.py  
python scripts/cross_language_table.py  
python scripts/cross_language_plot.py  
python scripts/stats_test.py  

---

## Limitations

- Random trees are unconstrained  
- No projectivity or linguistic constraints  

---

## Future Work

- Constrained random baselines  
- Projective tree models  
- Typology-aware models  

---

## Conclusion

Natural language is not random.

It systematically:
- minimizes dependency length  
- reduces structural interference  
- balances depth and branching  

However, global structure shows that language is shaped by **multiple competing constraints**, not a single optimization objective.

---

## Author

Pujit Sharath Shetty
