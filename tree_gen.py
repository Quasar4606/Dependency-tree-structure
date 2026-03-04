import random
from collections import defaultdict
import heapq


def generate_random_prufer(n):
    # Generate a random Prufer sequence of length n-2
    # Each value lies in [1, n]
    return [random.randint(1, n) for _ in range(n - 2)]


def prufer_to_tree_nsquare(prufer):
    # Source : https://www.geeksforgeeks.org/dsa/prufer-code-tree-creation/
    # This is O(n^2) algorithm

    n = len(prufer) + 2

    # degree[i] stores how many times node (i+1) appears in the code
    degree = [0] * n
    for i in range(n - 2):
        degree[prufer[i] - 1] += 1

    edges = []

    # Repeatedly attach smallest available leaf
    for i in range(n - 2):
        for j in range(n):
            if degree[j] == 0:
                degree[j] = -1
                degree[prufer[i] - 1] -= 1
                edges.append((j + 1, prufer[i]))
                break

    # Two nodes remain with degree 0
    remaining = [i + 1 for i in range(n) if degree[i] == 0]
    edges.append((remaining[0], remaining[1]))

    return edges


def prufer_to_tree_nlogn(prufer):
    # Source : https://cp-algorithms.com/graph/pruefer_code.html
    # This is O(n log n) algorithm , though the O(n^2) algorithm would have been sufficient

    n = len(prufer) + 2

    # Initialize all degrees to 1
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = 1

    # Increase degree according to Prufer sequence
    for v in prufer:
        degree[v] += 1

    # Min-heap to efficiently extract smallest leaf
    leaves = []
    for i in range(1, n + 1):
        if degree[i] == 1:
            heapq.heappush(leaves, i)

    edges = []

    for v in prufer:
        leaf = heapq.heappop(leaves)
        edges.append((leaf, v))

        degree[v] -= 1
        if degree[v] == 1:
            heapq.heappush(leaves, v)

    # Final two remaining leaves
    leaf1 = heapq.heappop(leaves)
    leaf2 = heapq.heappop(leaves)
    edges.append((leaf1, leaf2))

    return edges


def prufer_to_tree_n(prufer):
    # Source : https://cp-algorithms.com/graph/pruefer_code.html
    # This is O(n) algorithm , though O(n^2) algorithm would have been sufficient

    n = len(prufer) + 2

    # Initialize all degrees to 1
    degree = [0] * (n + 1)
    for i in range(1, n + 1):
        degree[i] = 1

    # Update degrees from Prufer sequence
    for v in prufer:
        degree[v] += 1

    # Find smallest initial leaf
    ptr = 1
    while degree[ptr] != 1:
        ptr += 1
    leaf = ptr

    edges = []

    for v in prufer:
        edges.append((leaf, v))
        degree[v] -= 1

        # If v becomes a leaf and is smaller than current pointer,
        # it becomes the next leaf
        if degree[v] == 1 and v < ptr:
            leaf = v
        else:
            ptr += 1
            while ptr <= n and degree[ptr] != 1:
                ptr += 1
            leaf = ptr

    # Connect last two remaining leaves
    edges.append((leaf, n))

    return edges


def make_directed_tree(edges, root):
    # Build adjacency list from undirected edges
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    directed_children = defaultdict(list)
    visited = set()

    # Depth-first search to direct edges away from root
    def dfs(node):
        visited.add(node)
        for neighbour in adj[node]:
            if neighbour not in visited:
                directed_children[node].append(neighbour)
                dfs(neighbour)

    dfs(root)
    return directed_children


def generate_random_tree(n):
    # Full pipeline:
    # 1. Sample random Prufer sequence
    # 2. Decode into undirected tree (O(n) version used)
    # 3. Choose random root
    # 4. Direct edges outward from root

    prufer = generate_random_prufer(n)
    edges = prufer_to_tree_n(prufer)  # using linear-time decoder
    root = random.randint(1, n)
    rand_children = make_directed_tree(edges, root)

    return root,rand_children