# from conllu import parse

# with open("en-sud-train.conllu", "r",encoding = "utf-8") as f:
#     data = f.read()

# sentences = parse(data)

# first_sentence = sentences[0]

# print("Sentences:")
# for token in first_sentence:
#     print(token["id"],token["form"], "->head:", token["head"])

from conllu import parse
from tree_gen import generate_random_tree

with open("en-sud-train.conllu", "r", encoding="utf-8") as f:
    data = f.read()

sentences = parse(data)
sentence = sentences[0]

parent = {}
children = {}

for token in sentence:
    idx = token["id"]
    parent[idx] = token["head"]
    children[idx] = []

for token in sentence:
    idx = token["id"]
    head = token["head"]
    if head != 0:
        children[head].append(idx)

print("Children structure:")
for node in children:
    print(node, "->", children[node])

root = None
for node in parent:
    if parent[node] == 0:
        root = node
        break

assert root != None

print("Root:",root)

def compute_depth(node,children):
    max_child_depth = 0
    for child in children[node]:
        d = compute_depth(child,children)
        max_child_depth = max(max_child_depth,d)
    return 1 + max_child_depth

depth = compute_depth(root,children)
print("Tree depth:",depth)

arity_values = []
for node in children:
    arity_values.append(len(children[node]))

non_zero = [a for a in arity_values if a > 0]

print("Arity per node:",arity_values)
print("Average arity:",sum(arity_values)/len(arity_values))
print("Max arity",max(arity_values))
print("Average arity(non-leaf):" ,sum(non_zero)/len(non_zero))
n = len(children)

rand_children = generate_random_tree(n)

rand_depth = compute_depth(1, rand_children)

print("Random depth:", rand_depth)