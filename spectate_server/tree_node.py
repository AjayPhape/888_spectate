def find_internal_nodes_num(tree):
    d = {}
    for pos, each in enumerate(tree):
        if each != -1:
            d.update({each: [*d.get(each, []), pos]})
    # print(len(set(tree)) -1)
    return len(d)


my_tree = [4, 4, 1, 5, -1, 4, 5]
print(find_internal_nodes_num(my_tree))
my_tree = [1, -1, 1, 1]
print(find_internal_nodes_num(my_tree))
my_tree = [6, 6, 1, 2, 5, 0, -1]
print(find_internal_nodes_num(my_tree))
