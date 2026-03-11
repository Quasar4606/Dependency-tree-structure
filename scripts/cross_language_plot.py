import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/cross_language_summary.csv")

# sort languages for cleaner plots
df = df.sort_values("Depth gap", ascending=False).reset_index(drop=True)

# -----------------------------
# 1. Depth gap across languages
# -----------------------------

plt.figure(figsize=(10,6))

plt.bar(df["Language"], df["Depth gap"], color="steelblue")

plt.ylabel("Average depth difference (Random − Real)")
plt.xlabel("Language")
plt.title("Depth gap across languages")

plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("results/cross_language_depth_gap.png")
plt.close()


# -----------------------------------------
# 2. Percent sentences where random deeper
# -----------------------------------------

plt.figure(figsize=(10,6))

plt.bar(df["Language"], df["Random deeper %"], color="darkorange")

plt.ylabel("Percent sentences where random tree is deeper")
plt.xlabel("Language")
plt.title("How often random trees are deeper")

plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("results/random_deeper_percentage.png")
plt.close()


# -----------------------------------------
# 3. Max arity comparison
# -----------------------------------------

x = range(len(df))

plt.figure(figsize=(10,6))

plt.bar(x, df["Real max arity"], width=0.4, label="Real", color="steelblue")
plt.bar([i + 0.4 for i in x], df["Random max arity"], width=0.4, label="Random", color="darkorange")

plt.xticks([i + 0.2 for i in x], df["Language"], rotation=45)

plt.ylabel("Average max arity")
plt.xlabel("Language")
plt.title("Branching comparison across languages")

plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("results/cross_language_arity_comparison.png")
plt.close()


# -----------------------------------------
# 4. Scatter: depth gap vs arity
# -----------------------------------------

plt.figure(figsize=(8,6))

plt.scatter(df["Depth gap"], df["Real max arity"], color="purple")

for i in range(len(df)):
    plt.text(
        df.iloc[i]["Depth gap"],
        df.iloc[i]["Real max arity"],
        df.iloc[i]["Language"],
        fontsize=9
    )

plt.xlabel("Depth gap (Random − Real)")
plt.ylabel("Real max arity")
plt.title("Relationship between tree depth and branching")

plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("results/depth_vs_arity_scatter.png")
plt.close()


print("Cross-language plots saved in results/")