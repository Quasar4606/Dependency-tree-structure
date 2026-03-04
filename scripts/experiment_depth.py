from conllu import parse
from src.tree_gen import generate_random_tree
from collections import defaultdict

with open("data/en-sud-train.conllu", "r", encoding="utf-8") as f:
    data = f.read()

sentences = parse(data)

real_depths = []
normalized_real_depths = []
random_depths = []
normalized_random_depths = []

#dfs
def compute_depth(node,children):
    max_child_depth = 0
    for child in children[node]:
        d = compute_depth(child,children)
        max_child_depth = max(max_child_depth,d)
    return 1 + max_child_depth

for sentence in sentences:
    parent = {}
    children = defaultdict(list)
    for token in sentence:
        idx = token["id"]
        parent[idx] = token["head"]
        children[idx] = []
    for token in sentence:
        idx = token["id"]
        head = token["head"]
        if head != 0:
            children[head].append(idx)
    n = len(children)
    if n < 3 :
        continue
    root = None
    for node in parent:
        if parent[node] == 0:
            root = node
            break
    assert root != None
    real_depth = compute_depth(root,children)
    real_depths.append(real_depth)
    normalized_real_depths.append(real_depth/n)
    rand_root,rand_children = generate_random_tree(n)
    rand_depth = compute_depth(rand_root,rand_children)
    random_depths.append(rand_depth)
    normalized_random_depths.append(rand_depth/n)

avg_real = sum(real_depths) / len(real_depths)
avg_random = sum(random_depths) / len(random_depths)

avg_real_norm = sum(normalized_real_depths) / len(normalized_real_depths)
avg_random_norm = sum(normalized_random_depths) / len(normalized_random_depths)

print("Sentences processed:", len(real_depths))
print("Average real depth:", avg_real)
print("Average random depth:", avg_random)

print("Average normalized real depth:", avg_real_norm)
print("Average normalized random depth:", avg_random_norm)