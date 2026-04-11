import os
import csv
import random
from conllu import parse

from src.tree_gen import generate_random_tree
from src.dep_tree import build_tree
from src.metrics import (
    compute_depth,
    compute_average_depth,
    compute_max_arity,
    compute_degree_entropy,
    compute_dependency_length,
    compute_random_tree_dl,
    compute_ic,
    compute_wic,
    compute_random_tree_ic,
    compute_random_tree_wic,
    compute_pic_all_pairs_from_children,
    compute_avg_lca_depth
)

random.seed(42)

DATA_DIR = "data"
RESULT_DIR = "results"
NUM_RANDOM = 20

os.makedirs(RESULT_DIR, exist_ok=True)


for file in os.listdir(DATA_DIR):

    if not file.endswith(".conllu"):
        continue

    language = file.split("-")[0]
    data_path = os.path.join(DATA_DIR, file)

    print("\n==============================")
    print(f"Processing language: {language}")
    print("==============================")

    with open(data_path, "r", encoding="utf-8") as f:
        sentences = parse(f.read())

    # containers
    real_metrics = []
    random_metrics = []
    results = []

    for sentence in sentences:
        try:
            root, children = build_tree(sentence)
        except ValueError:
            continue

        n = len(children)
        if n < 3:
            continue

        # ---------- REAL ----------
        real = {
            "depth": compute_depth(root, children),
            "avg_depth": compute_average_depth(root, children),
            "arity": compute_max_arity(children),
            "entropy": compute_degree_entropy(children),
            "dl": compute_dependency_length(sentence),
            "ic": compute_ic(sentence),
            "wic": compute_wic(sentence),
            "pic": compute_pic_all_pairs_from_children(children),
            "lca": compute_avg_lca_depth(children)
        }

        # ---------- RANDOM ----------
        rand_acc = {k: 0 for k in real}

        for _ in range(NUM_RANDOM):
            rand_root, rand_children = generate_random_tree(n)

            rand_acc["depth"] += compute_depth(rand_root, rand_children)
            rand_acc["avg_depth"] += compute_average_depth(rand_root, rand_children)
            rand_acc["arity"] += compute_max_arity(rand_children)
            rand_acc["entropy"] += compute_degree_entropy(rand_children)
            rand_acc["dl"] += compute_random_tree_dl(rand_children)
            rand_acc["ic"] += compute_random_tree_ic(rand_children)
            rand_acc["wic"] += compute_random_tree_wic(rand_children)
            rand_acc["pic"] += compute_pic_all_pairs_from_children(rand_children)
            rand_acc["lca"] += compute_avg_lca_depth(rand_children)

        rand = {k: rand_acc[k] / NUM_RANDOM for k in rand_acc}

        real_metrics.append(real)
        random_metrics.append(rand)

        results.append({
            "n": n,
            **{f"real_{k}": v for k, v in real.items()},
            **{f"random_{k}": v for k, v in rand.items()}
        })

    # -----------------------------
    # aggregate
    # -----------------------------
    def avg(lst, key):
        return sum(x[key] for x in lst) / len(lst)

    print("\nSentences processed:", len(real_metrics))

    for key in ["depth", "avg_depth", "arity", "entropy", "dl", "ic", "wic", "pic", "lca"]:
        print(f"\n--- {key.upper()} ---")
        print("Real:", avg(real_metrics, key))
        print("Random:", avg(random_metrics, key))

    # -----------------------------
    # sanity checks
    # -----------------------------
    print("\n--- Sanity Checks ---")

    def percent_random_higher(metric):
        return sum(
            1 for i in range(len(real_metrics))
            if random_metrics[i][metric] > real_metrics[i][metric]
        ) / len(real_metrics) * 100

    def percent_real_higher(metric):
        return sum(
            1 for i in range(len(real_metrics))
            if real_metrics[i][metric] > random_metrics[i][metric]
        ) / len(real_metrics) * 100

    # metrics where lower is better
    for m in ["depth", "dl", "ic", "wic"]:
        print(f"Random higher ({m}): {percent_random_higher(m):.2f}")

    # PIC: higher is interpreted as stronger structure
    print(f"Real higher (pic): {percent_real_higher('pic'):.2f}")

    # -----------------------------
    # save CSV
    # -----------------------------
    lang_result_dir = os.path.join(RESULT_DIR, language)
    os.makedirs(lang_result_dir, exist_ok=True)

    output_file = os.path.join(lang_result_dir, "results_full.csv")

    keys = ["depth", "avg_depth", "arity", "entropy", "dl", "ic", "wic", "pic", "lca"]

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(
            ["length"] +
            [f"real_{k}" for k in keys] +
            [f"random_{k}" for k in keys]
        )

        for r in results:
            writer.writerow(
                [r["n"]] +
                [r[f"real_{k}"] for k in keys] +
                [r[f"random_{k}"] for k in keys]
            )