import os
import pandas as pd

RESULT_DIR = "results"

# dedicated folder for cross-language outputs
CROSS_DIR = os.path.join(RESULT_DIR, "cross_language")
os.makedirs(CROSS_DIR, exist_ok=True)

rows = []

# collect summary statistics for each language
for language in os.listdir(RESULT_DIR):

    if language == "cross_language":
        continue

    lang_path = os.path.join(RESULT_DIR, language)
    csv_path = os.path.join(lang_path, "results_full.csv")  # UPDATED

    if not os.path.exists(csv_path):
        continue

    df = pd.read_csv(csv_path)

    if len(df) == 0:
        continue

    # -----------------------------
    # Depth
    # -----------------------------
    real_depth = df["real_depth"].mean()
    random_depth = df["random_depth"].mean()
    depth_gap = (df["random_depth"] - df["real_depth"]).mean()
    random_deeper = (df["random_depth"] > df["real_depth"]).mean() * 100

    # -----------------------------
    # Average Depth
    # -----------------------------
    real_avg_depth = df["real_avg_depth"].mean()
    random_avg_depth = df["random_avg_depth"].mean()

    # -----------------------------
    # Dependency Length (MOST IMPORTANT)
    # -----------------------------
    real_dl = df["real_dl"].mean()
    random_dl = df["random_dl"].mean()
    dl_gap = (df["random_dl"] - df["real_dl"]).mean()
    random_dl_higher = (df["random_dl"] > df["real_dl"]).mean() * 100

    # -----------------------------
    # Branching
    # -----------------------------
    real_arity = df["real_max_arity"].mean()
    random_arity = df["random_max_arity"].mean()

    rows.append({
        "Language": language.capitalize(),
        "Sentences": len(df),

        "Depth Gap": depth_gap,
        "Random Deeper (%)": random_deeper,

        "Avg Depth (Real)": real_avg_depth,
        "Avg Depth (Random)": random_avg_depth,

        "DL Gap": dl_gap,
        "Random DL Higher (%)": random_dl_higher,

        "Real Max Arity": real_arity,
        "Random Max Arity": random_arity
    })

# create table
table = pd.DataFrame(rows)

# sort by strongest signal (DL gap is best)
table = table.sort_values("DL Gap", ascending=False).reset_index(drop=True)

# round for readability
table = table.round(3)

# print nicely
print("\nCross-language summary:\n")
print(table.to_string(index=False))

# save
output_path = os.path.join(CROSS_DIR, "cross_language_summary.csv")
table.to_csv(output_path, index=False)

print(f"\nSaved summary to: {output_path}")