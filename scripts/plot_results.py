import os
import pandas as pd
import matplotlib.pyplot as plt

RESULT_DIR = "results"

# iterate over each language folder
for language in os.listdir(RESULT_DIR):

    lang_path = os.path.join(RESULT_DIR, language)
    csv_path = os.path.join(lang_path, "results_full.csv")  # UPDATED FILE

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

    plt.figure(figsize=(8,5))

    plt.plot(depth_grouped.index, depth_grouped["real_mean"],
             label="Real", linewidth=2, color="steelblue")

    plt.plot(depth_grouped.index, depth_grouped["random_mean"],
             label="Random", linewidth=2, color="darkorange")

    plt.xlabel("Sentence Length")
    plt.ylabel("Average Tree Depth")
    plt.title(f"Depth vs Sentence Length — {language.capitalize()}")

    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.savefig(os.path.join(lang_path, "depth_vs_length.png"))
    plt.close()

    # -----------------------------
    # Average depth vs length (NEW)
    # -----------------------------
    avg_depth_grouped = df.groupby("length").agg({
        "real_avg_depth": ["mean", "count"],
        "random_avg_depth": "mean"
    })

    avg_depth_grouped.columns = ["real_mean", "count", "random_mean"]
    avg_depth_grouped = avg_depth_grouped[avg_depth_grouped["count"] >= 20]

    plt.figure(figsize=(8,5))

    plt.plot(avg_depth_grouped.index, avg_depth_grouped["real_mean"],
             label="Real", linewidth=2, color="steelblue")

    plt.plot(avg_depth_grouped.index, avg_depth_grouped["random_mean"],
             label="Random", linewidth=2, color="darkorange")

    plt.xlabel("Sentence Length")
    plt.ylabel("Average Depth")
    plt.title(f"Average Depth vs Length — {language.capitalize()}")

    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.savefig(os.path.join(lang_path, "avg_depth_vs_length.png"))
    plt.close()

    # -----------------------------
    # Dependency Length vs length (NEW, IMPORTANT)
    # -----------------------------
    dl_grouped = df.groupby("length").agg({
        "real_dl": ["mean", "count"],
        "random_dl": "mean"
    })

    dl_grouped.columns = ["real_mean", "count", "random_mean"]
    dl_grouped = dl_grouped[dl_grouped["count"] >= 20]

    plt.figure(figsize=(8,5))

    plt.plot(dl_grouped.index, dl_grouped["real_mean"],
             label="Real", linewidth=2, color="steelblue")

    plt.plot(dl_grouped.index, dl_grouped["random_mean"],
             label="Random", linewidth=2, color="darkorange")

    plt.xlabel("Sentence Length")
    plt.ylabel("Dependency Length")
    plt.title(f"Dependency Length vs Length — {language.capitalize()}")

    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.savefig(os.path.join(lang_path, "dl_vs_length.png"))
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

    plt.figure(figsize=(8,5))

    plt.plot(arity_grouped.index, arity_grouped["real_mean"],
             label="Real", linewidth=2, color="steelblue")

    plt.plot(arity_grouped.index, arity_grouped["random_mean"],
             label="Random", linewidth=2, color="darkorange")

    plt.xlabel("Sentence Length")
    plt.ylabel("Average Max Arity")
    plt.title(f"Branching vs Sentence Length — {language.capitalize()}")

    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.savefig(os.path.join(lang_path, "arity_vs_length.png"))
    plt.close()

    # -----------------------------
    # Max arity distribution
    # -----------------------------
    plt.figure(figsize=(8,5))

    plt.hist(df["real_max_arity"], bins=15, alpha=0.6,
             label="Real", color="steelblue")

    plt.hist(df["random_max_arity"], bins=15, alpha=0.6,
             label="Random", color="darkorange")

    plt.xlabel("Max Arity")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of Branching — {language.capitalize()}")

    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.savefig(os.path.join(lang_path, "arity_distribution.png"))
    plt.close()

    # -----------------------------
    # Dependency Length distribution (NEW)
    # -----------------------------
    plt.figure(figsize=(8,5))

    plt.hist(df["real_dl"], bins=30, alpha=0.6,
             label="Real", color="steelblue")

    plt.hist(df["random_dl"], bins=30, alpha=0.6,
             label="Random", color="darkorange")

    plt.xlabel("Dependency Length")
    plt.ylabel("Frequency")
    plt.title(f"Dependency Length Distribution — {language.capitalize()}")

    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.savefig(os.path.join(lang_path, "dl_distribution.png"))
    plt.close()

    # -----------------------------
    # Depth gap histogram
    # -----------------------------
    df["depth_gap"] = df["random_depth"] - df["real_depth"]

    plt.figure(figsize=(8,5))

    plt.hist(df["depth_gap"], bins=30, color="purple")

    plt.xlabel("Random Depth − Real Depth")
    plt.ylabel("Frequency")
    plt.title(f"Depth Difference — {language.capitalize()}")

    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.savefig(os.path.join(lang_path, "depth_gap.png"))
    plt.close()

    # -----------------------------
    # Dependency Length gap (NEW)
    # -----------------------------
    df["dl_gap"] = df["random_dl"] - df["real_dl"]

    plt.figure(figsize=(8,5))

    plt.hist(df["dl_gap"], bins=30, color="green")

    plt.xlabel("Random DL − Real DL")
    plt.ylabel("Frequency")
    plt.title(f"Dependency Length Difference — {language.capitalize()}")

    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.savefig(os.path.join(lang_path, "dl_gap.png"))
    plt.close()

    # -----------------------------
    # Quick summary
    # -----------------------------
    print("Average depth gap:", round(df["depth_gap"].mean(), 3))
    print("Percent random deeper:",
          round((df["random_depth"] > df["real_depth"]).mean() * 100, 2))

    print("Average DL gap:", round(df["dl_gap"].mean(), 3))
    print("Percent random DL higher:",
          round((df["random_dl"] > df["real_dl"]).mean() * 100, 2))