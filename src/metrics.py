# Basic structural measurements for dependency trees

import math
import random
from collections import Counter


# -----------------------------
# Depth Metrics
# -----------------------------

def compute_depth(node, children):
    # DFS to find the longest root-to-leaf path (max depth)
    max_child_depth = 0

    for child in children[node]:
        depth = compute_depth(child, children)
        max_child_depth = max(max_child_depth, depth)

    return 1 + max_child_depth


def _collect_depths(node, children, current_depth, depths):
    depths.append(current_depth)
    for child in children[node]:
        _collect_depths(child, children, current_depth + 1, depths)


def compute_average_depth(root, children):
    # Average depth of all nodes from root
    depths = []
    _collect_depths(root, children, 1, depths)
    return sum(depths) / len(depths)


# -----------------------------
# Arity / Degree Metrics
# -----------------------------

def compute_max_arity(children):
    # maximum number of children any node has
    return max(len(children[node]) for node in children)


def compute_arities(children):
    # return list of branching factors for all nodes
    return [len(children[node]) for node in children]


def compute_degree_entropy(children):
    # entropy of degree (number of children) distribution
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
    # average dependency length for real sentence
    total = 0
    count = 0

    for token in sentence:
        # skip multiword tokens
        if not isinstance(token["id"], int):
            continue

        head = token["head"]

        # skip root
        if head == 0:
            continue

        total += abs(token["id"] - head)
        count += 1

    return total / count if count > 0 else 0


def compute_random_tree_dl(children):
    # assign random positions to nodes and compute dependency length
    nodes = list(children.keys())
    n = len(nodes)

    positions = list(range(1, n + 1))
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
# Utility
# -----------------------------

def count_nodes(children):
    # total number of nodes in the tree
    return len(children)