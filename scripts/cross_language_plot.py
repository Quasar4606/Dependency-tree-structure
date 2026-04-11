import os
import pandas as pd
import matplotlib.pyplot as plt

CROSS_DIR = os.path.join("results", "cross_language")
os.makedirs(CROSS_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(CROSS_DIR, "cross_language_summary.csv"))

# -----------------------------
# Detect columns
# -----------------------------
PIC_GAP = "PIC Gap (Real−Random)"
DL_GAP = "DL Gap (Random−Real)"
DEPTH_GAP = "DEPTH Gap (Random−Real)"
IC_GAP = "IC Gap (Random−Real)"
WIC_GAP = "WIC Gap (Random−Real)"
LCA_GAP = "LCA Gap (Random−Real)"

PIC_DOM = "PIC Real Higher (%)"
DL_DOM = "DL Random Higher (%)"
DEPTH_DOM = "DEPTH Random Higher (%)"

ARITY_REAL = "ARITY (Real)"
DEPTH_REAL = "DEPTH (Real)"

# -----------------------------
# sort
# -----------------------------
if DL_GAP in df.columns:
    df = df.sort_values(DL_GAP, ascending=False)
elif PIC_GAP in df.columns:
    df = df.sort_values(PIC_GAP, ascending=False)

df = df.reset_index(drop=True)

# -----------------------------
# 1. DL GAP
# -----------------------------
if DL_GAP in df.columns:
    plt.figure(figsize=(10,6))
    plt.bar(df["Language"], df[DL_GAP])
    plt.title("Dependency Length Gap Across Languages")
    plt.ylabel("Random − Real")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CROSS_DIR, "cross_language_dl_gap.png"))
    plt.close()

# -----------------------------
# 2. DEPTH GAP 
# -----------------------------
if DEPTH_GAP in df.columns:
    plt.figure(figsize=(10,6))
    plt.bar(df["Language"], df[DEPTH_GAP])
    plt.title("Tree Depth Gap Across Languages")
    plt.ylabel("Random − Real")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CROSS_DIR, "cross_language_depth_gap.png"))
    plt.close()

# -----------------------------
# 3. PIC GAP
# -----------------------------
if PIC_GAP in df.columns:
    plt.figure(figsize=(10,6))
    plt.bar(df["Language"], df[PIC_GAP])
    plt.title("PIC Gap Across Languages")
    plt.ylabel("Real − Random")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CROSS_DIR, "cross_language_pic_gap.png"))
    plt.close()

# -----------------------------
# 4. IC / WIC GAP
# -----------------------------
for metric, col in [("IC", IC_GAP), ("WIC", WIC_GAP)]:
    if col not in df.columns:
        continue

    plt.figure(figsize=(10,6))
    plt.bar(df["Language"], df[col])
    plt.title(f"{metric} Gap Across Languages")
    plt.ylabel("Random − Real")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CROSS_DIR, f"cross_language_{metric.lower()}_gap.png"))
    plt.close()

# -----------------------------
# 5. LCA GAP
# -----------------------------
if LCA_GAP in df.columns:
    plt.figure(figsize=(10,6))
    plt.bar(df["Language"], df[LCA_GAP])
    plt.title("LCA Depth Gap Across Languages")
    plt.ylabel("Random − Real")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CROSS_DIR, "cross_language_lca_gap.png"))
    plt.close()

# -----------------------------
# 6. DL DOMINANCE 
# -----------------------------
if DL_DOM in df.columns:
    plt.figure(figsize=(10,6))
    plt.bar(df["Language"], df[DL_DOM])
    plt.title("Random Higher % (DL)")
    plt.ylabel("%")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CROSS_DIR, "random_dl_higher_percentage.png"))
    plt.close()

# -----------------------------
# 7. DEPTH DOMINANCE 
# -----------------------------
if DEPTH_DOM in df.columns:
    plt.figure(figsize=(10,6))
    plt.bar(df["Language"], df[DEPTH_DOM])
    plt.title("Random Deeper %")
    plt.ylabel("%")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CROSS_DIR, "random_deeper_percentage.png"))
    plt.close()

# -----------------------------
# 8. PIC DOMINANCE
# -----------------------------
if PIC_DOM in df.columns:
    plt.figure(figsize=(10,6))
    plt.bar(df["Language"], df[PIC_DOM])
    plt.title("Real Higher % (PIC)")
    plt.ylabel("%")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CROSS_DIR, "pic_dominance.png"))
    plt.close()

# -----------------------------
# 9. DL vs PIC SCATTER
# -----------------------------
if DL_GAP in df.columns and PIC_GAP in df.columns:
    plt.figure(figsize=(8,6))
    plt.scatter(df[DL_GAP], df[PIC_GAP], s=70)

    for i in range(len(df)):
        plt.text(df.iloc[i][DL_GAP], df.iloc[i][PIC_GAP], df.iloc[i]["Language"], fontsize=9)

    plt.xlabel("DL Gap")
    plt.ylabel("PIC Gap")
    plt.title("DL vs PIC")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CROSS_DIR, "dl_vs_pic_scatter.png"))
    plt.close()

# -----------------------------
# 10. DEPTH vs ARITY SCATTER 
# -----------------------------
if DEPTH_REAL in df.columns and ARITY_REAL in df.columns:
    plt.figure(figsize=(8,6))
    plt.scatter(df[DEPTH_REAL], df[ARITY_REAL], s=70)

    for i in range(len(df)):
        plt.text(df.iloc[i][DEPTH_REAL], df.iloc[i][ARITY_REAL], df.iloc[i]["Language"], fontsize=9)

    plt.xlabel("Depth (Real)")
    plt.ylabel("Arity (Real)")
    plt.title("Depth vs Arity Across Languages")

    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CROSS_DIR, "depth_vs_arity_scatter.png"))
    plt.close()

# -----------------------------
# ARITY COMPARISON 
# -----------------------------
if "ARITY (Real)" in df.columns and "ARITY (Random)" in df.columns:

    x = range(len(df))
    width = 0.35

    plt.figure(figsize=(10,6))

    plt.bar(x, df["ARITY (Real)"], width, label="Real")
    plt.bar([i + width for i in x], df["ARITY (Random)"], width, label="Random")

    plt.xticks([i + width/2 for i in x], df["Language"], rotation=45)

    plt.ylabel("Maximum Arity")
    plt.title("Arity Comparison Across Languages")

    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(CROSS_DIR, "cross_language_arity_comparison.png"))
    plt.close()

# -----------------------------
# DEPTH vs ARITY SCATTER 
# -----------------------------
if "DEPTH (Real)" in df.columns and "ARITY (Real)" in df.columns:

    plt.figure(figsize=(8,6))

    plt.scatter(df["DEPTH (Real)"], df["ARITY (Real)"], s=70)

    for i in range(len(df)):
        plt.text(
            df.iloc[i]["DEPTH (Real)"],
            df.iloc[i]["ARITY (Real)"],
            df.iloc[i]["Language"],
            fontsize=9
        )

    plt.xlabel("Tree Depth (Real)")
    plt.ylabel("Maximum Arity (Real)")
    plt.title("Depth vs Arity Across Languages")

    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(CROSS_DIR, "depth_vs_arity_scatter.png"))
    plt.close()

print(f"Saved all cross-language plots in {CROSS_DIR}/")