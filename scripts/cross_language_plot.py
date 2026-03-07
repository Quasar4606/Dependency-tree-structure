import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/cross_language_summary.csv")

# sort languages by depth gap for clearer plots
df = df.sort_values("Depth gap", ascending=False)

# -----------------------------
# 1. Depth gap across languages
# -----------------------------

plt.figure(figsize=(10,6))

plt.bar(df["Language"], df["Depth gap"])

plt.ylabel("Average depth difference (Random − Real)")
plt.xlabel("Language")
plt.title("Depth gap across languages")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("results/cross_language_depth_gap.png")
plt.close()


# -----------------------------------------
# 2. Percent sentences where random deeper
# -----------------------------------------

plt.figure(figsize=(10,6))

plt.bar(df["Language"], df["Random deeper %"])

plt.ylabel("Percent sentences where random tree is deeper")
plt.xlabel("Language")
plt.title("How often random trees are deeper")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("results/random_deeper_percentage.png")
plt.close()


# -----------------------------------------
# 3. Max arity comparison
# -----------------------------------------

x = range(len(df))

plt.figure(figsize=(10,6))

plt.bar(x, df["Real max arity"], width=0.4, label="Real", align="center")
plt.bar([i + 0.4 for i in x], df["Random max arity"], width=0.4, label="Random")

plt.xticks([i + 0.2 for i in x], df["Language"], rotation=45)

plt.ylabel("Average max arity")
plt.xlabel("Language")
plt.title("Branching comparison across languages")

plt.legend()

plt.tight_layout()

plt.savefig("results/cross_language_arity_comparison.png")
plt.close()


# -----------------------------------------
# 4. Scatter: depth gap vs arity
# -----------------------------------------

plt.figure(figsize=(8,6))

plt.scatter(df["Depth gap"], df["Real max arity"])

for i, lang in enumerate(df["Language"]):
    plt.text(df["Depth gap"][i], df["Real max arity"][i], lang)

plt.xlabel("Depth gap (Random − Real)")
plt.ylabel("Real max arity")
plt.title("Relationship between tree depth and branching")

plt.tight_layout()

plt.savefig("results/depth_vs_arity_scatter.png")
plt.close()


print("Cross-language plots saved in results/")