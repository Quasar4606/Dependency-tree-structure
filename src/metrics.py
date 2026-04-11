# Basic structural measurements for dependency trees

import math
import random
from collections import Counter
from src.dep_tree import build_tree


# -----------------------------
# Depth Metrics
# -----------------------------

def compute_depth(node, children):
    # DFS: longest root-to-leaf path
    max_child_depth = 0
    for child in children[node]:
        depth = compute_depth(child, children)
        max_child_depth = max(max_child_depth, depth)
    return 1 + max_child_depth


def _collect_depths(node, children, current_depth, depths):
    # collect depth of each node
    depths.append(current_depth)
    for child in children[node]:
        _collect_depths(child, children, current_depth + 1, depths)


def compute_average_depth(root, children):
    # average depth across nodes
    depths = []
    _collect_depths(root, children, 1, depths)
    return sum(depths) / len(depths)


# -----------------------------
# Arity / Degree Metrics
# -----------------------------

def compute_max_arity(children):
    # maximum branching factor
    return max(len(children[node]) for node in children)


def compute_arities(children):
    # list of degrees
    return [len(children[node]) for node in children]


def compute_degree_entropy(children):
    # entropy of degree distribution
    degrees = [len(children[node]) for node in children]
    freq = Counter(degrees)
    total = len(degrees)

    entropy = 0
    for count in freq.values():
        p = count / total
        entropy -= p * math.log(p)

    return entropy


# -----------------------------
# Dependency Length Metrics
# -----------------------------

def compute_dependency_length(sentence):
    # average linear distance between head and dependent
    total = 0
    count = 0

    for token in sentence:
        if not isinstance(token["id"], int):
            continue

        h = token["head"]
        if h == 0:
            continue

        total += abs(token["id"] - h)
        count += 1

    return total / count if count > 0 else 0


def compute_random_tree_dl(children):
    # random linear order → compute DL
    nodes = list(children.keys())

    positions = list(range(1, len(nodes) + 1))
    random.shuffle(positions)
    pos = {node: positions[i] for i, node in enumerate(nodes)}

    total = 0
    count = 0

    for parent in children:
        for child in children[parent]:
            total += abs(pos[parent] - pos[child])
            count += 1

    return total / count if count > 0 else 0


# -----------------------------
# Intervener Complexity Metrics
# -----------------------------

def compute_ic(sentence):
    # count heads between dependency endpoints
    _, children = build_tree(sentence)

    head_flag = {node: 1 if len(children[node]) > 0 else 0 for node in children}

    # prefix sum over sentence order
    prefix = {}
    running = 0
    for i in sorted(head_flag.keys()):
        running += head_flag[i]
        prefix[i] = running

    total_ic = 0
    count = 0

    for token in sentence:
        if not isinstance(token["id"], int):
            continue

        h = token["head"]
        d = token["id"]
        if h == 0:
            continue

        l, r = min(h, d), max(h, d)

        ic = 0 if r - l <= 1 else prefix.get(r - 1, 0) - prefix.get(l, 0)

        total_ic += ic
        count += 1

    return total_ic / count if count > 0 else 0


def compute_wic(sentence):
    # weighted IC (using outdegree)
    _, children = build_tree(sentence)

    weights = {node: len(children[node]) for node in children}

    prefix = {}
    running = 0
    for i in sorted(weights.keys()):
        running += weights[i]
        prefix[i] = running

    total_wic = 0
    count = 0

    for token in sentence:
        if not isinstance(token["id"], int):
            continue

        h = token["head"]
        d = token["id"]
        if h == 0:
            continue

        l, r = min(h, d), max(h, d)

        wic = 0 if r - l <= 1 else prefix.get(r - 1, 0) - prefix.get(l, 0)

        total_wic += wic
        count += 1

    return total_wic / count if count > 0 else 0


def compute_random_tree_ic(children):
    # IC under random ordering (O(n^2))
    nodes = list(children.keys())

    positions = list(range(1, len(nodes) + 1))
    random.shuffle(positions)
    pos = {node: positions[i] for i, node in enumerate(nodes)}

    is_head = {node: len(children[node]) > 0 for node in children}

    total_ic = 0
    count = 0

    for parent in children:
        for child in children[parent]:
            h, d = pos[parent], pos[child]
            l, r = min(h, d), max(h, d)

            ic = 0
            for node in nodes:
                p = pos[node]
                if l < p < r and is_head[node]:
                    ic += 1

            total_ic += ic
            count += 1

    return total_ic / count if count > 0 else 0


def compute_random_tree_wic(children):
    # WIC under random ordering (O(n^2))
    nodes = list(children.keys())

    positions = list(range(1, len(nodes) + 1))
    random.shuffle(positions)
    pos = {node: positions[i] for i, node in enumerate(nodes)}

    outdegree = {node: len(children[node]) for node in children}

    total_wic = 0
    count = 0

    for parent in children:
        for child in children[parent]:
            h, d = pos[parent], pos[child]
            l, r = min(h, d), max(h, d)

            wic = 0
            for node in nodes:
                p = pos[node]
                if l < p < r and outdegree[node] > 0:
                    wic += outdegree[node]

            total_wic += wic
            count += 1

    return total_wic / count if count > 0 else 0


# -----------------------------
# Path Integration Cost (PIC)
# -----------------------------

def compute_pic_all_pairs_from_children(children):
    # compute PIC via node contributions (O(n))

    nodes = list(children.keys())
    n = len(nodes)

    # find root
    all_children = set(c for v in children for c in children[v])
    root = next(v for v in children if v not in all_children)

    f = {node: len(children[node]) for node in children}

    subtree = {}

    def dfs(node):
        size = 1
        for child in children[node]:
            size += dfs(child)
        subtree[node] = size
        return size

    dfs(root)

    total_pic = 0

    for v in children:
        # components formed when removing v
        components = [subtree[c] for c in children[v]]

        parent_side = n - subtree[v]
        if parent_side > 0:
            components.append(parent_side)

        # count pairs crossing v
        total = n - 1
        sum_sq = sum(x * x for x in components)

        pairs = (total * total - sum_sq) // 2

        total_pic += f[v] * pairs

    total_pairs = n * (n - 1) // 2
    return total_pic / total_pairs if total_pairs > 0 else 0


# -----------------------------
# Average LCA Depth
# -----------------------------

def compute_avg_lca_depth(children):
    # average depth of LCA over all pairs (O(n))

    nodes = list(children.keys())
    n = len(nodes)

    all_children = set(c for v in children for c in children[v])
    root = next(v for v in children if v not in all_children)

    subtree = {}
    depth = {}

    def dfs(node, d):
        depth[node] = d
        size = 1
        for child in children[node]:
            size += dfs(child, d + 1)
        subtree[node] = size
        return size

    dfs(root, 0)

    total = 0

    for v in children:
        # only child subtrees matter for LCA
        components = [subtree[c] for c in children[v]]

        total_size = sum(components)
        sum_sq = sum(x * x for x in components)

        pairs = (total_size * total_size - sum_sq) // 2
        pairs += (subtree[v] - 1)
        total += depth[v] * pairs

    total_pairs = n * (n - 1) // 2
    return total / total_pairs if total_pairs > 0 else 0


# -----------------------------
# Utility
# -----------------------------

def count_nodes(children):
    return len(children)