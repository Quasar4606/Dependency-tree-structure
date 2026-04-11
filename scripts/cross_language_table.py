import os
import pandas as pd

RESULT_DIR = "results"

CROSS_DIR = os.path.join(RESULT_DIR, "cross_language")
os.makedirs(CROSS_DIR, exist_ok=True)

rows = []

METRICS = ["depth", "avg_depth", "arity", "entropy", "dl", "ic", "wic", "pic", "lca"]

for language in os.listdir(RESULT_DIR):

    if language == "cross_language":
        continue

    lang_path = os.path.join(RESULT_DIR, language)
    csv_path = os.path.join(lang_path, "results_full.csv")

    if not os.path.exists(csv_path):
        continue

    df = pd.read_csv(csv_path)

    if len(df) == 0:
        continue

    row = {
        "Language": language.capitalize(),
        "Sentences": len(df)
    }

    for m in METRICS:
        real_col = f"real_{m}"
        rand_col = f"random_{m}"

        if real_col not in df or rand_col not in df:
            continue

        real_mean = df[real_col].mean()
        rand_mean = df[rand_col].mean()

        if m == "pic":
            gap = (df[real_col] - df[rand_col]).mean()
            pct = (df[real_col] > df[rand_col]).mean() * 100
            gap_name = f"{m.upper()} Gap (Real−Random)"
            pct_name = f"{m.upper()} Real Higher (%)"
        else:
            gap = (df[rand_col] - df[real_col]).mean()
            pct = (df[rand_col] > df[real_col]).mean() * 100
            gap_name = f"{m.upper()} Gap (Random−Real)"
            pct_name = f"{m.upper()} Random Higher (%)"

        row[f"{m.upper()} (Real)"] = real_mean
        row[f"{m.upper()} (Random)"] = rand_mean
        row[gap_name] = gap
        row[pct_name] = pct

    rows.append(row)

# -----------------------------
# Create dataframe
# -----------------------------
table = pd.DataFrame(rows)

#  sort by strongest signal 
if "DL Gap (Random−Real)" in table.columns:
    table = table.sort_values("DL Gap (Random−Real)", ascending=False)
elif "PIC Gap (Real−Random)" in table.columns:
    table = table.sort_values("PIC Gap (Real−Random)", ascending=False)

table = table.reset_index(drop=True)
table = table.round(3)

# -----------------------------
# Print 
# -----------------------------
print("\nCross-language summary:\n")
print(table.to_string(index=False))

# -----------------------------
# Save CSV
# -----------------------------
output_path = os.path.join(CROSS_DIR, "cross_language_summary.csv")
table.to_csv(output_path, index=False)

print(f"\nSaved summary to: {output_path}")