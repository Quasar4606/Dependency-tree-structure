# Basic structural measurements for dependency trees


def compute_depth(node, children):
    # DFS to find the longest root-to-leaf path
    max_child_depth = 0

    for child in children[node]:
        depth = compute_depth(child, children)
        max_child_depth = max(max_child_depth, depth)

    return 1 + max_child_depth


def compute_max_arity(children):
    # maximum number of children any node has
    return max(len(children[node]) for node in children)


def compute_arities(children):
    # return list of branching factors for all nodes
    return [len(children[node]) for node in children]


def count_nodes(children):
    # total number of nodes in the tree
    return len(children)