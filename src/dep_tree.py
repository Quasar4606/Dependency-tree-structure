from collections import defaultdict


def extract_parent_map(sentence):
    # Map each token id to its syntactic head
    parent = {}

    for token in sentence:
        if not isinstance(token["id"], int):
            continue
        parent[token["id"]] = token["head"]

    return parent


def build_children(parent):
    # Convert parent map -> adjacency list (node -> children)
    children = defaultdict(list)

    # initialize nodes
    for node in parent:
        children[node] = []

    # attach each node to its parent
    for node, head in parent.items():
        if head != 0:  # head == 0 means root
            children[head].append(node)

    return children


def find_root(parent):
    # In CoNLL-U format the root has head = 0
    for node, head in parent.items():
        if head == 0:
            return node

    raise ValueError("No root found in sentence")


def build_tree(sentence):
    """
    Build a dependency tree from a parsed CoNLL-U sentence.

    Returns
    -------
    root : int
        root node id

    children : dict
        adjacency list (node -> list of children)
    """

    parent = extract_parent_map(sentence)
    children = build_children(parent)
    root = find_root(parent)

    return root, children