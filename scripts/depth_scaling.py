import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

RESULT_DIR = "results"

# dedicated folder for cross-language outputs
CROSS_DIR = os.path.join(RESULT_DIR, "cross_language")
os.makedirs(CROSS_DIR, exist_ok=True)

rows = []

# loop over languages
for language in os.listdir(RESULT_DIR):

    # skip cross_language folder itself
    if language == "cross_language":
        continue

    csv_path = os.path.join(RESULT_DIR, language, "results_depth.csv")

    if not os.path.exists(csv_path):
        continue

    df = pd.read_csv(csv_path)

    # remove very small sentences (unstable for log)
    df = df[df["length"] >= 3]

    if len(df) == 0:
        continue

    # log-transform
    x = np.log(df["length"])
    y_real = np.log(df["real_depth"])
    y_rand = np.log(df["random_depth"])

    # linear fit in log-log space
    real_slope = np.polyfit(x, y_real, 1)[0]
    rand_slope = np.polyfit(x, y_rand, 1)[0]

    rows.append({
        "Language": language.capitalize(),
        "Real Exponent": real_slope,
        "Random Exponent": rand_slope
    })

# create table
table = pd.DataFrame(rows)
table = table.round(3)

print("\nDepth scaling summary:\n")
print(table.to_string(index=False))

# save results
table.to_csv(os.path.join(CROSS_DIR, "depth_scaling_summary.csv"), index=False)

# -----------------------------
# Plot comparison
# -----------------------------

x = range(len(table))

plt.figure(figsize=(10,6))

plt.bar(x, table["Real Exponent"], width=0.4,
        label="Real", color="steelblue")

plt.bar([i + 0.4 for i in x], table["Random Exponent"], width=0.4,
        label="Random", color="darkorange")

plt.xticks([i + 0.2 for i in x], table["Language"], rotation=45)

plt.ylabel("Scaling Exponent (b)")
plt.xlabel("Language")
plt.title("Depth Scaling Across Languages")

plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(os.path.join(CROSS_DIR, "depth_scaling.png"))
plt.close()

print(f"\nSaved depth scaling results in {CROSS_DIR}/")