import os
import pandas as pd
from scipy.stats import ttest_rel, mannwhitneyu

RESULT_DIR = "results"

CROSS_DIR = os.path.join(RESULT_DIR, "cross_language")
os.makedirs(CROSS_DIR, exist_ok=True)

summary = []

# all metrics 
METRICS = [
    "depth",
    "avg_depth",
    "arity",
    "entropy",
    "dl",
    "ic",
    "wic",
    "pic",
    "lca"
]

for language in os.listdir(RESULT_DIR):

    if language == "cross_language":
        continue

    csv_path = os.path.join(RESULT_DIR, language, "results_full.csv")

    if not os.path.exists(csv_path):
        continue

    df = pd.read_csv(csv_path)

    if len(df) == 0:
        continue

    row = {"Language": language.capitalize()}

    print(f"\n=== {language.upper()} ===")

    for metric in METRICS:
        real_col = f"real_{metric}"
        rand_col = f"random_{metric}"

        if real_col not in df or rand_col not in df:
            continue

        real_vals = df[real_col]
        rand_vals = df[rand_col]

        # paired t-test
        t_stat, p_t = ttest_rel(real_vals, rand_vals)

        # Mann-Whitney
        _, p_mw = mannwhitneyu(real_vals, rand_vals, alternative="two-sided")

        # direction (IMPORTANT)
        if metric == "pic":
            diff = (real_vals - rand_vals).mean()  # flipped
            direction = "Real > Random"
        else:
            diff = (rand_vals - real_vals).mean()
            direction = "Random > Real"

        row[f"{metric.upper()} diff"] = diff
        row[f"{metric.upper()} p"] = p_t
        row[f"{metric.upper()} MW p"] = p_mw

        print(f"{metric.upper()} p={p_t:.3e} | {direction} | diff={diff:.3f}")

    summary.append(row)


# dataframe
summary_df = pd.DataFrame(summary)

# save
summary_df.to_csv(os.path.join(CROSS_DIR, "statistical_tests.csv"), index=False)

print(f"\nSaved statistical tests in {CROSS_DIR}/")