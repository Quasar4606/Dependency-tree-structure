from conllu import parse
from src.tree_gen import generate_random_tree
from src.dep_tree import build_tree
from src.metrics import compute_depth,compute_max_arity
# from collections import defaultdict
import csv
import random

random.seed(42)

DATA_PATH = "data/en-sud-train.conllu"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = f.read()

sentences = parse(data)

real_depths = []
normalized_real_depths = []
random_depths = []
normalized_random_depths = []
depth_dif = []
max_real_arities = []
max_rand_arities = []
results = []
# depth_by_len_real = defaultdict(list)
# depth_by_len_rand = defaultdict(list)
# max_arity_by_len_real = defaultdict(list)
# max_arity_by_len_rand = defaultdict(list)
NUM_RANDOM = 20

for sentence in sentences:
    root,children = build_tree(sentence)
    n = len(children)
    if n < 3 :
        continue
    real_depth = compute_depth(root,children)
    real_depths.append(real_depth)
    normalized_real_depths.append(real_depth/n)
    rand_depths = []
    rand_arities = []
    for _ in range(NUM_RANDOM):
        rand_root , rand_children = generate_random_tree(n)
        rand_depths.append(compute_depth(rand_root,rand_children))
        rand_arities.append(compute_max_arity(rand_children))
    rand_depth = sum(rand_depths) / NUM_RANDOM
    random_depths.append(rand_depth)
    normalized_random_depths.append(rand_depth/n)
    depth_dif.append(rand_depth - real_depth)
    max_real_arity = compute_max_arity(children)
    max_rand_arity = sum(rand_arities) / NUM_RANDOM
    max_real_arities.append(max_real_arity)
    max_rand_arities.append(max_rand_arity)
    results.append({
        "n": n,
        "real_depth": real_depth,
        "random_depth": rand_depth,
        "real_arity": max_real_arity,
        "random_arity": max_rand_arity
    })
    # depth_by_len_real[n].append(real_depth)
    # depth_by_len_rand[n].append(rand_depth)

    # max_arity_by_len_real[n].append(max_real_arity)
    # max_arity_by_len_rand[n].append(max_rand_arity)

avg_real = sum(real_depths) / len(real_depths)
avg_random = sum(random_depths) / len(random_depths)

avg_real_norm = sum(normalized_real_depths) / len(normalized_real_depths)
avg_random_norm = sum(normalized_random_depths) / len(normalized_random_depths)

print("Sentences processed:", len(real_depths))
print("\n")
print("Depth statistics")
print("-----------------------------")
print("Average real depth:", avg_real)
print("Average random depth:", avg_random)

print("Average normalized real depth:", avg_real_norm)
print("Average normalized random depth:", avg_random_norm)

avg_diff = sum(depth_dif)/len(depth_dif)

count_random_deeper = sum(1 for d in depth_dif if d > 0)
percentage_random_deeper = count_random_deeper / len(depth_dif) * 100

print("Average depth difference:",avg_diff)
print(f"Random deeper in {percentage_random_deeper}% of sentences")
print("\n")
print("Branching Statistics")
print("-----------------------------")

# real_arity_dist = Counter(real_arities)
# random_arity_dist = Counter(random_arities)
# print("Real arity distribution:", real_arity_dist)
# print("Random arity distribution:", random_arity_dist)

avg_max_real_arity = sum(max_real_arities) / len(max_real_arities)
avg_max_rand_arity = sum(max_rand_arities) / len(max_rand_arities)

print("Average max real arity:" , avg_max_real_arity)
print("Average max random arity:",avg_max_rand_arity)

# for n in sorted(depth_by_len_real):
#     avg_real = sum(depth_by_len_real[n]) / len(depth_by_len_real[n])
#     avg_rand = sum(depth_by_len_rand[n]) / len(depth_by_len_rand[n])
#     avg_real_a = sum(max_arity_by_len_real[n]) / len(max_arity_by_len_real[n])
#     avg_rand_a = sum(max_arity_by_len_rand[n]) / len(max_arity_by_len_rand[n])
#     print(n, avg_real, avg_rand, avg_real_a, avg_rand_a)

with open("results/results_depth.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["length","real_depth","random_depth","real_max_arity","random_max_arity"])
    
    for r in results:
        writer.writerow([
            r["n"],
            r["real_depth"],
            r["random_depth"],
            r["real_arity"],
            r["random_arity"]
        ])