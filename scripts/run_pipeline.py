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
    compute_random_tree_dl
)

# fix randomness so results are reproducible across runs
random.seed(42)

DATA_DIR = "data"
RESULT_DIR = "results"
NUM_RANDOM = 20  # number of random trees per sentence

# ensure results folder exists
os.makedirs(RESULT_DIR, exist_ok=True)


# loop over all datasets (each file corresponds to one language)
for file in os.listdir(DATA_DIR):

    if not file.endswith(".conllu"):
        continue

    language = file.split("-")[0]
    data_path = os.path.join(DATA_DIR, file)

    print("\n==============================")
    print(f"Processing language: {language}")
    print("==============================")

    # read and parse dependency trees
    with open(data_path, "r", encoding="utf-8") as f:
        data = f.read()

    sentences = parse(data)

    # -----------------------------
    # containers for statistics
    # -----------------------------
    real_depths = []
    random_depths = []

    real_avg_depths = []
    random_avg_depths = []

    real_dls = []
    random_dls = []

    real_entropies = []
    random_entropies = []

    max_real_arities = []
    max_rand_arities = []

    results = []

    # -----------------------------
    # process each sentence
    # -----------------------------
    for sentence in sentences:
        try:
            root, children = build_tree(sentence)
        except ValueError:
            continue

        n = len(children)

        if n < 3:
            continue

        # ----- REAL TREE METRICS -----
        real_depth = compute_depth(root, children)
        real_avg_depth = compute_average_depth(root, children)
        real_arity = compute_max_arity(children)
        real_entropy = compute_degree_entropy(children)
        real_dl = compute_dependency_length(sentence)

        real_depths.append(real_depth)
        real_avg_depths.append(real_avg_depth)
        real_entropies.append(real_entropy)
        real_dls.append(real_dl)
        max_real_arities.append(real_arity)

        # ----- RANDOM TREE METRICS -----
        rand_depths = []
        rand_avg_depths = []
        rand_arities = []
        rand_entropies = []
        rand_dls = []

        for _ in range(NUM_RANDOM):
            rand_root, rand_children = generate_random_tree(n)

            rand_depths.append(compute_depth(rand_root, rand_children))
            rand_avg_depths.append(compute_average_depth(rand_root, rand_children))
            rand_arities.append(compute_max_arity(rand_children))
            rand_entropies.append(compute_degree_entropy(rand_children))
            rand_dls.append(compute_random_tree_dl(rand_children))

        # average random metrics
        rand_depth = sum(rand_depths) / NUM_RANDOM
        rand_avg_depth = sum(rand_avg_depths) / NUM_RANDOM
        rand_arity = sum(rand_arities) / NUM_RANDOM
        rand_entropy = sum(rand_entropies) / NUM_RANDOM
        rand_dl = sum(rand_dls) / NUM_RANDOM

        random_depths.append(rand_depth)
        random_avg_depths.append(rand_avg_depth)
        random_entropies.append(rand_entropy)
        random_dls.append(rand_dl)
        max_rand_arities.append(rand_arity)

        # store per-sentence results
        results.append({
            "n": n,
            "real_depth": real_depth,
            "random_depth": rand_depth,
            "real_avg_depth": real_avg_depth,
            "random_avg_depth": rand_avg_depth,
            "real_arity": real_arity,
            "random_arity": rand_arity,
            "real_entropy": real_entropy,
            "random_entropy": rand_entropy,
            "real_dl": real_dl,
            "random_dl": rand_dl
        })

    # -----------------------------
    # aggregate statistics
    # -----------------------------
    def avg(x): return sum(x) / len(x)

    print("\nSentences processed:", len(real_depths))

    print("\n--- Depth ---")
    print("Real:", avg(real_depths))
    print("Random:", avg(random_depths))

    print("\n--- Average Depth ---")
    print("Real:", avg(real_avg_depths))
    print("Random:", avg(random_avg_depths))

    print("\n--- Dependency Length ---")
    print("Real:", avg(real_dls))
    print("Random:", avg(random_dls))

    print("\n--- Degree Entropy ---")
    print("Real:", avg(real_entropies))
    print("Random:", avg(random_entropies))

    print("\n--- Max Arity ---")
    print("Real:", avg(max_real_arities))
    print("Random:", avg(max_rand_arities))

    # sanity signals
    print("\n--- Sanity Checks ---")
    print("Random deeper %:",
          sum(1 for i in range(len(real_depths)) if random_depths[i] > real_depths[i]) / len(real_depths) * 100)

    print("Random DL higher %:",
          sum(1 for i in range(len(real_dls)) if random_dls[i] > real_dls[i]) / len(real_dls) * 100)

    # -----------------------------
    # save results
    # -----------------------------
    lang_result_dir = os.path.join(RESULT_DIR, language)
    os.makedirs(lang_result_dir, exist_ok=True)

    output_file = os.path.join(lang_result_dir, "results_full.csv")

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "length",
            "real_depth", "random_depth",
            "real_avg_depth", "random_avg_depth",
            "real_max_arity", "random_max_arity",
            "real_entropy", "random_entropy",
            "real_dl", "random_dl"
        ])

        for r in results:
            writer.writerow([
                r["n"],
                r["real_depth"], r["random_depth"],
                r["real_avg_depth"], r["random_avg_depth"],
                r["real_arity"], r["random_arity"],
                r["real_entropy"], r["random_entropy"],
                r["real_dl"], r["random_dl"]
            ])