import os
import pandas as pd

RESULT_DIR = "results"

rows = []

for language in os.listdir(RESULT_DIR):

    csv_path = os.path.join(RESULT_DIR, language, "results_depth.csv")

    if not os.path.exists(csv_path):
        continue

    df = pd.read_csv(csv_path)

    real_depth = df["real_depth"].mean()
    random_depth = df["random_depth"].mean()

    depth_gap = (df["random_depth"] - df["real_depth"]).mean()

    random_deeper = (df["random_depth"] > df["real_depth"]).mean() * 100

    real_arity = df["real_max_arity"].mean()
    random_arity = df["random_max_arity"].mean()

    rows.append({
        "Language": language,
        "Sentences": len(df),
        "Real depth": real_depth,
        "Random depth": random_depth,
        "Depth gap": depth_gap,
        "Random deeper %": random_deeper,
        "Real max arity": real_arity,
        "Random max arity": random_arity
    })

table = pd.DataFrame(rows)

table = table.sort_values("Depth gap", ascending=False)

print(table)

table.to_csv("results/cross_language_summary.csv", index=False)