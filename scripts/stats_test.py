import os
import pandas as pd
from scipy.stats import ttest_rel, mannwhitneyu

RESULT_DIR = "results"

# dedicated folder
CROSS_DIR = os.path.join(RESULT_DIR, "cross_language")
os.makedirs(CROSS_DIR, exist_ok=True)

summary = []

# iterate over languages
for language in os.listdir(RESULT_DIR):

    if language == "cross_language":
        continue

    csv_path = os.path.join(RESULT_DIR, language, "results_depth.csv")

    if not os.path.exists(csv_path):
        continue

    df = pd.read_csv(csv_path)

    if len(df) == 0:
        continue

    # depth tests
    t_stat_d, t_p_d = ttest_rel(df["real_depth"], df["random_depth"])

    _, u_p_d = mannwhitneyu(
        df["real_depth"],
        df["random_depth"],
        alternative="two-sided"
    )

    # arity tests
    t_stat_a, t_p_a = ttest_rel(df["real_max_arity"], df["random_max_arity"])

    _, u_p_a = mannwhitneyu(
        df["real_max_arity"],
        df["random_max_arity"],
        alternative="two-sided"
    )

    summary.append({
        "Language": language.capitalize(),
        "Depth t-stat": round(t_stat_d, 3),
        "Depth p-value": t_p_d,
        "Depth MW p-value": u_p_d,
        "Arity t-stat": round(t_stat_a, 3),
        "Arity p-value": t_p_a,
        "Arity MW p-value": u_p_a
    })

    print(f"\n=== {language.upper()} ===")
    print(f"Depth p={t_p_d:.3e}, Arity p={t_p_a:.3e}")

# create table
summary_df = pd.DataFrame(summary)

# save to cross_language folder
summary_df.to_csv(os.path.join(CROSS_DIR, "statistical_tests.csv"), index=False)

print(f"\nSaved statistical tests in {CROSS_DIR}/")