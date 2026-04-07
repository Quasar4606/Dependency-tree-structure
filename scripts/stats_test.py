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

    csv_path = os.path.join(RESULT_DIR, language, "results_full.csv")  # UPDATED

    if not os.path.exists(csv_path):
        continue

    df = pd.read_csv(csv_path)

    if len(df) == 0:
        continue

    # -----------------------------
    # Depth
    # -----------------------------
    t_d, p_d = ttest_rel(df["real_depth"], df["random_depth"])
    _, mw_d = mannwhitneyu(df["real_depth"], df["random_depth"], alternative="two-sided")

    # -----------------------------
    # Average Depth
    # -----------------------------
    t_ad, p_ad = ttest_rel(df["real_avg_depth"], df["random_avg_depth"])
    _, mw_ad = mannwhitneyu(df["real_avg_depth"], df["random_avg_depth"], alternative="two-sided")

    # -----------------------------
    # Dependency Length (MOST IMPORTANT)
    # -----------------------------
    t_dl, p_dl = ttest_rel(df["real_dl"], df["random_dl"])
    _, mw_dl = mannwhitneyu(df["real_dl"], df["random_dl"], alternative="two-sided")

    # -----------------------------
    # Max Arity
    # -----------------------------
    t_a, p_a = ttest_rel(df["real_max_arity"], df["random_max_arity"])
    _, mw_a = mannwhitneyu(df["real_max_arity"], df["random_max_arity"], alternative="two-sided")

    # -----------------------------
    # Entropy (optional interpretation)
    # -----------------------------
    t_e, p_e = ttest_rel(df["real_entropy"], df["random_entropy"])
    _, mw_e = mannwhitneyu(df["real_entropy"], df["random_entropy"], alternative="two-sided")

    summary.append({
        "Language": language.capitalize(),

        "Depth p": p_d,
        "Avg Depth p": p_ad,
        "Dependency Length p": p_dl,
        "Arity p": p_a,
        "Entropy p": p_e,

        "Depth MW p": mw_d,
        "Avg Depth MW p": mw_ad,
        "DL MW p": mw_dl,
        "Arity MW p": mw_a,
        "Entropy MW p": mw_e
    })

    print(f"\n=== {language.upper()} ===")
    print(f"Depth p={p_d:.3e}")
    print(f"Avg Depth p={p_ad:.3e}")
    print(f"DL p={p_dl:.3e}")
    print(f"Arity p={p_a:.3e}")
    print(f"Entropy p={p_e:.3e}")

# create table
summary_df = pd.DataFrame(summary)

# save to cross_language folder
summary_df.to_csv(os.path.join(CROSS_DIR, "statistical_tests.csv"), index=False)

print(f"\nSaved statistical tests in {CROSS_DIR}/")