import os
import pandas as pd

RESULT_DIR = "results"

# dedicated folder for cross-language outputs
CROSS_DIR = os.path.join(RESULT_DIR, "cross_language")
os.makedirs(CROSS_DIR, exist_ok=True)

rows = []

# collect summary statistics for each language
for language in os.listdir(RESULT_DIR):

    lang_path = os.path.join(RESULT_DIR, language)

    # skip the cross_language folder itself
    if language == "cross_language":
        continue

    csv_path = os.path.join(lang_path, "results_depth.csv")

    if not os.path.exists(csv_path):
        continue

    df = pd.read_csv(csv_path)

    # skip empty files just in case
    if len(df) == 0:
        continue

    # basic averages
    real_depth = df["real_depth"].mean()
    random_depth = df["random_depth"].mean()

    # how much deeper random trees are on average
    depth_gap = (df["random_depth"] - df["real_depth"]).mean()

    # percentage of sentences where random tree is deeper
    random_deeper = (df["random_depth"] > df["real_depth"]).mean() * 100

    # branching comparison
    real_arity = df["real_max_arity"].mean()
    random_arity = df["random_max_arity"].mean()

    rows.append({
        "Language": language.capitalize(),
        "Sentences": len(df),
        "Real Depth": real_depth,
        "Random Depth": random_depth,
        "Depth Gap": depth_gap,
        "Random Deeper (%)": random_deeper,
        "Real Max Arity": real_arity,
        "Random Max Arity": random_arity
    })

# create table
table = pd.DataFrame(rows)

# sort languages by strongest depth difference
table = table.sort_values("Depth Gap", ascending=False).reset_index(drop=True)

# round values for readability
table = table.round(3)

# print nicely (for quick inspection)
print("\nCross-language summary:\n")
print(table.to_string(index=False))

# save inside cross_language folder
output_path = os.path.join(CROSS_DIR, "cross_language_summary.csv")
table.to_csv(output_path, index=False)

print(f"\nSaved summary to: {output_path}")