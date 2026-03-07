import os
import pandas as pd
import matplotlib.pyplot as plt

RESULT_DIR = "results"

for language in os.listdir(RESULT_DIR):

    lang_path = os.path.join(RESULT_DIR, language)
    csv_path = os.path.join(lang_path, "results_depth.csv")

    if not os.path.exists(csv_path):
        continue

    print(f"\nProcessing plots for: {language}")

    df = pd.read_csv(csv_path)

    # -----------------------------
    # Depth vs sentence length
    # -----------------------------

    depth_grouped = df.groupby("length").agg({
        "real_depth": ["mean", "count"],
        "random_depth": "mean"
    })

    depth_grouped.columns = ["real_mean", "count", "random_mean"]

    depth_grouped = depth_grouped[depth_grouped["count"] >= 20]

    plt.figure()

    plt.plot(depth_grouped.index, depth_grouped["real_mean"], label="Real")
    plt.plot(depth_grouped.index, depth_grouped["random_mean"], label="Random")

    plt.xlabel("Sentence length")
    plt.ylabel("Average tree depth")
    plt.title(f"Depth vs sentence length ({language})")

    plt.legend()

    plt.savefig(os.path.join(lang_path, "depth_curve.png"))

    plt.close()

    # -----------------------------
    # Max arity vs sentence length
    # -----------------------------

    arity_grouped = df.groupby("length").agg({
        "real_max_arity": ["mean", "count"],
        "random_max_arity": "mean"
    })

    arity_grouped.columns = ["real_mean", "count", "random_mean"]

    arity_grouped = arity_grouped[arity_grouped["count"] >= 20]

    plt.figure()

    plt.plot(arity_grouped.index, arity_grouped["real_mean"], label="Real")
    plt.plot(arity_grouped.index, arity_grouped["random_mean"], label="Random")

    plt.xlabel("Sentence length")
    plt.ylabel("Average max arity")
    plt.title(f"Branching vs sentence length ({language})")

    plt.legend()

    plt.savefig(os.path.join(lang_path, "arity_curve.png"))

    plt.close()

    # -----------------------------
    # Max arity distribution
    # -----------------------------

    plt.figure()

    plt.hist(df["real_max_arity"], bins=15, alpha=0.6, label="Real")
    plt.hist(df["random_max_arity"], bins=15, alpha=0.6, label="Random")

    plt.xlabel("Max arity")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of max branching ({language})")

    plt.legend()

    plt.savefig(os.path.join(lang_path, "arity_distribution.png"))

    plt.close()

    # -----------------------------
    # Depth gap histogram
    # -----------------------------

    df["depth_gap"] = df["random_depth"] - df["real_depth"]

    plt.figure()

    plt.hist(df["depth_gap"], bins=30)

    plt.xlabel("Random depth − Real depth")
    plt.ylabel("Frequency")
    plt.title(f"Depth difference ({language})")

    plt.savefig(os.path.join(lang_path, "depth_gap.png"))

    plt.close()

    # -----------------------------
    # Summary statistics
    # -----------------------------

    print("Average depth gap:", df["depth_gap"].mean())
    print("Percent random deeper:",
          (df["random_depth"] > df["real_depth"]).mean() * 100)