import os
import csv
import random
from conllu import parse

from src.tree_gen import generate_random_tree
from src.dep_tree import build_tree
from src.metrics import compute_depth, compute_max_arity

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

    # containers for statistics
    real_depths = []
    normalized_real_depths = []
    random_depths = []
    normalized_random_depths = []
    depth_dif = []
    max_real_arities = []
    max_rand_arities = []
    results = []

    # process each sentence independently
    for sentence in sentences:
        try:
            root, children = build_tree(sentence)
        except ValueError:
            # skip malformed trees (rare but happens)
            continue

        n = len(children)

        # ignore very small trees (not meaningful structurally)
        if n < 3:
            continue

        # compute depth for the real dependency tree
        real_depth = compute_depth(root, children)

        real_depths.append(real_depth)
        normalized_real_depths.append(real_depth / n)

        rand_depths = []
        rand_arities = []

        # generate multiple random trees of same size
        for _ in range(NUM_RANDOM):
            rand_root, rand_children = generate_random_tree(n)

            rand_depths.append(compute_depth(rand_root, rand_children))
            rand_arities.append(compute_max_arity(rand_children))

        # average over random samples to reduce variance
        rand_depth = sum(rand_depths) / NUM_RANDOM

        random_depths.append(rand_depth)
        normalized_random_depths.append(rand_depth / n)

        # difference between random and real depth
        depth_dif.append(rand_depth - real_depth)

        # branching (max number of children of any node)
        max_real = compute_max_arity(children)
        max_rand = sum(rand_arities) / NUM_RANDOM

        max_real_arities.append(max_real)
        max_rand_arities.append(max_rand)

        # store per-sentence results (used later for plotting)
        results.append({
            "n": n,
            "real_depth": real_depth,
            "random_depth": rand_depth,
            "real_arity": max_real,
            "random_arity": max_rand
        })

    # compute aggregate statistics for the language
    avg_real = sum(real_depths) / len(real_depths)
    avg_random = sum(random_depths) / len(random_depths)

    avg_real_norm = sum(normalized_real_depths) / len(normalized_real_depths)
    avg_random_norm = sum(normalized_random_depths) / len(normalized_random_depths)

    avg_diff = sum(depth_dif) / len(depth_dif)

    count_random_deeper = sum(1 for d in depth_dif if d > 0)
    percentage_random_deeper = count_random_deeper / len(depth_dif) * 100

    avg_max_real = sum(max_real_arities) / len(max_real_arities)
    avg_max_rand = sum(max_rand_arities) / len(max_rand_arities)

    # print quick summary for sanity check
    print("Sentences processed:", len(real_depths))
    print("\nDepth statistics")
    print("-----------------------------")
    print("Average real depth:", avg_real)
    print("Average random depth:", avg_random)
    print("Average normalized real depth:", avg_real_norm)
    print("Average normalized random depth:", avg_random_norm)
    print("Average depth difference:", avg_diff)
    print(f"Random deeper in {percentage_random_deeper}% of sentences")

    print("\nBranching Statistics")
    print("-----------------------------")
    print("Average max real arity:", avg_max_real)
    print("Average max random arity:", avg_max_rand)

    # create a separate folder for each language
    lang_result_dir = os.path.join(RESULT_DIR, language)
    os.makedirs(lang_result_dir, exist_ok=True)

    output_file = os.path.join(lang_result_dir, "results_depth.csv")

    # save per-sentence results (used by plotting scripts later)
    with open(output_file, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "length",
            "real_depth",
            "random_depth",
            "real_max_arity",
            "random_max_arity"
        ])

        for r in results:
            writer.writerow([
                r["n"],
                r["real_depth"],
                r["random_depth"],
                r["real_arity"],
                r["random_arity"]
            ])