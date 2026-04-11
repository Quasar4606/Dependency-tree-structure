import os
import pandas as pd
import matplotlib.pyplot as plt

RESULT_DIR = "results"

# -----------------------------
# LENGTH-BASED PLOTS
# -----------------------------
LENGTH_METRICS = [
    ("depth", "Tree Depth"),
    ("avg_depth", "Average Depth"),
    ("arity", "Maximum Arity"),
    ("entropy", "Degree Entropy"),
    ("dl", "Dependency Length"),
    ("ic", "Intervener Complexity"),
    ("wic", "Weighted IC"),
    ("pic", "Path Integration Cost"),
    ("lca", "Average LCA Depth"),
]

# -----------------------------
# DISTRIBUTIONS 
# -----------------------------
DIST_METRICS = [
    ("arity", "Maximum Arity"),  # ← added
    ("dl", "Dependency Length"),
    ("ic", "IC"),
    ("wic", "WIC"),
    ("pic", "PIC"),
]

# -----------------------------
# GAP METRICS
# -----------------------------
GAP_METRICS = [
    "depth",
    "arity",
    "dl",
    "ic",
    "wic",
    "pic"
]

for language in os.listdir(RESULT_DIR):

    lang_path = os.path.join(RESULT_DIR, language)
    csv_path = os.path.join(lang_path, "results_full.csv")

    if not os.path.exists(csv_path):
        continue

    print(f"\nProcessing plots for: {language}")

    df = pd.read_csv(csv_path)

    # =============================
    # LENGTH-BASED PLOTS
    # =============================
    for metric, label in LENGTH_METRICS:

        real_col = f"real_{metric}"
        rand_col = f"random_{metric}"

        if real_col not in df or rand_col not in df:
            continue

        grouped = df.groupby("length").agg({
            real_col: ["mean", "count"],
            rand_col: "mean"
        })

        grouped.columns = ["real_mean", "count", "random_mean"]
        grouped = grouped[grouped["count"] >= 20]

        plt.figure(figsize=(8, 5))

        plt.plot(grouped.index, grouped["real_mean"], linewidth=2, label="Real")
        plt.plot(grouped.index, grouped["random_mean"], linewidth=2, label="Random")

        plt.xlabel("Sentence Length")
        plt.ylabel(label)
        plt.title(f"{label} vs Length — {language.capitalize()}")

        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()

        plt.savefig(os.path.join(lang_path, f"{metric}_vs_length.png"))
        plt.close()

    # =============================
    # DISTRIBUTION PLOTS 
    # =============================
    for metric, label in DIST_METRICS:

        real_col = f"real_{metric}"
        rand_col = f"random_{metric}"

        if real_col not in df or rand_col not in df:
            continue

        plt.figure(figsize=(8, 5))

        plt.hist(df[real_col], bins=30, alpha=0.6, label="Real")
        plt.hist(df[rand_col], bins=30, alpha=0.6, label="Random")

        plt.xlabel(label)
        plt.ylabel("Frequency")
        plt.title(f"{label} Distribution — {language.capitalize()}")

        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()

        plt.savefig(os.path.join(lang_path, f"{metric}_distribution.png"))
        plt.close()

    # =============================
    # GAP PLOTS
    # =============================
    for metric in GAP_METRICS:

        real_col = f"real_{metric}"
        rand_col = f"random_{metric}"

        if real_col not in df or rand_col not in df:
            continue

        if metric == "pic":
            gap = df[real_col] - df[rand_col]
            xlabel = f"Real − Random ({metric.upper()})"
        else:
            gap = df[rand_col] - df[real_col]
            xlabel = f"Random − Real ({metric.upper()})"

        plt.figure(figsize=(8, 5))
        plt.hist(gap, bins=30)

        plt.xlabel(xlabel)
        plt.ylabel("Frequency")
        plt.title(f"{metric.upper()} Gap — {language.capitalize()}")

        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()

        plt.savefig(os.path.join(lang_path, f"{metric}_gap.png"))
        plt.close()

        print(f"{metric.upper()} gap mean:", round(gap.mean(), 3))

        if metric == "pic":
            percent = (df[real_col] > df[rand_col]).mean() * 100
            print(f"Real higher % ({metric}):", round(percent, 2))
        else:
            percent = (df[rand_col] > df[real_col]).mean() * 100
            print(f"Random higher % ({metric}):", round(percent, 2))