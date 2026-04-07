import os
import pandas as pd
import matplotlib.pyplot as plt

# directory for cross-language outputs
CROSS_DIR = os.path.join("results", "cross_language")
os.makedirs(CROSS_DIR, exist_ok=True)

# load summary table
df = pd.read_csv(os.path.join(CROSS_DIR, "cross_language_summary.csv"))

# sort by strongest signal (DL is best metric)
df = df.sort_values("DL Gap", ascending=False).reset_index(drop=True)

# -----------------------------
# 1. Dependency Length Gap (MOST IMPORTANT)
# -----------------------------
plt.figure(figsize=(10,6))

plt.bar(df["Language"], df["DL Gap"], color="seagreen")

plt.ylabel("Dependency Length Difference (Random − Real)")
plt.xlabel("Language")
plt.title("Dependency Length Gap Across Languages")

plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(os.path.join(CROSS_DIR, "cross_language_dl_gap.png"))
plt.close()


# -----------------------------
# 2. Depth gap across languages
# -----------------------------
plt.figure(figsize=(10,6))

plt.bar(df["Language"], df["Depth Gap"], color="steelblue")

plt.ylabel("Depth Difference (Random − Real)")
plt.xlabel("Language")
plt.title("Depth Difference Across Languages")

plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(os.path.join(CROSS_DIR, "cross_language_depth_gap.png"))
plt.close()


# -----------------------------------------
# 3. How often random trees are deeper
# -----------------------------------------
plt.figure(figsize=(10,6))

plt.bar(df["Language"], df["Random Deeper (%)"], color="darkorange")

plt.ylabel("Percent (Random > Real)")
plt.xlabel("Language")
plt.title("Frequency of Random Trees Being Deeper")

plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(os.path.join(CROSS_DIR, "random_deeper_percentage.png"))
plt.close()


# -----------------------------------------
# 4. Dependency Length dominance (NEW)
# -----------------------------------------
plt.figure(figsize=(10,6))

plt.bar(df["Language"], df["Random DL Higher (%)"], color="green")

plt.ylabel("Percent (Random DL > Real DL)")
plt.xlabel("Language")
plt.title("Dependency Length Dominance Across Languages")

plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(os.path.join(CROSS_DIR, "random_dl_higher_percentage.png"))
plt.close()


# -----------------------------------------
# 5. Max arity comparison
# -----------------------------------------
x = range(len(df))

plt.figure(figsize=(10,6))

plt.bar(x, df["Real Max Arity"], width=0.4,
        label="Real", color="steelblue")

plt.bar([i + 0.4 for i in x], df["Random Max Arity"], width=0.4,
        label="Random", color="darkorange")

plt.xticks([i + 0.2 for i in x], df["Language"], rotation=45)

plt.ylabel("Average Max Arity")
plt.xlabel("Language")
plt.title("Branching Comparison Across Languages")

plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(os.path.join(CROSS_DIR, "cross_language_arity_comparison.png"))
plt.close()


# -----------------------------------------
# 6. Scatter: depth vs branching
# -----------------------------------------
plt.figure(figsize=(8,6))

plt.scatter(df["Depth Gap"], df["Real Max Arity"],
            color="purple", s=60)

for i in range(len(df)):
    plt.text(
        df.iloc[i]["Depth Gap"],
        df.iloc[i]["Real Max Arity"],
        df.iloc[i]["Language"],
        fontsize=9
    )

plt.xlabel("Depth Gap")
plt.ylabel("Real Max Arity")
plt.title("Depth vs Branching Relationship")

plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(os.path.join(CROSS_DIR, "depth_vs_arity_scatter.png"))
plt.close()


print(f"Saved cross-language plots in {CROSS_DIR}/")