import os
import pandas as pd
from scipy.stats import ttest_rel, mannwhitneyu

RESULT_DIR = "results"

summary = []

for language in os.listdir(RESULT_DIR):

    csv_path = os.path.join(RESULT_DIR, language, "results_depth.csv")

    if not os.path.exists(csv_path):
        continue

    df = pd.read_csv(csv_path)

    # -----------------------------
    # DEPTH TESTS
    # -----------------------------

    t_stat_d, t_p_d = ttest_rel(df["real_depth"], df["random_depth"])
    u_stat_d, u_p_d = mannwhitneyu(df["real_depth"], df["random_depth"])

    # -----------------------------
    # MAX ARITY TESTS
    # -----------------------------

    t_stat_a, t_p_a = ttest_rel(df["real_max_arity"], df["random_max_arity"])
    u_stat_a, u_p_a = mannwhitneyu(df["real_max_arity"], df["random_max_arity"])

    summary.append({
        "language": language,
        "depth_t_stat": t_stat_d,
        "depth_t_p": t_p_d,
        "depth_mw_p": u_p_d,
        "arity_t_stat": t_stat_a,
        "arity_t_p": t_p_a,
        "arity_mw_p": u_p_a
    })

    print(language)
    print("Depth t-test:", t_stat_d, t_p_d)
    print("Depth Mann-Whitney:", u_p_d)
    print("Arity t-test:", t_stat_a, t_p_a)
    print("Arity Mann-Whitney:", u_p_a)
    print()

summary_df = pd.DataFrame(summary)

summary_df.to_csv("results/statistical_tests.csv", index=False)