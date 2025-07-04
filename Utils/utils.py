from tabulate import tabulate


def clean_expr(expr, prefixes):
    output_str = str(expr)
    for tc in prefixes:
        output_str = output_str.replace(tc, "")
    return output_str


def print_df(df):
    print(tabulate(df, headers='keys', tablefmt='psql'))


def print_dict(d, prefixes):
    for key, val in d.items():
        print(f"\t{clean_expr(str(key), prefixes)} -> {clean_expr(str(val), prefixes)}")


def print_list(input_list, prefixes):
    for el in input_list:
        print(f"\t{clean_expr(el, prefixes)}")


def printNTree(x, flag, depth, isLast, T, vertex_depths):
    #     print(f"x = {x}, depth = {depth}, isLast = {isLast}")
    if x is None:
        return

    i = 1
    while i < depth:
        i += 1
        if flag[i]:
            print("|   ", end=' ')
        else:
            print("    ", end=' ')

    #   Condition when the current node is the root node
    if depth == 0:
        print(T.V[x].name)
    elif isLast:
        # print(f"+--- {T.V[x].name}")
        roleToPrint = ""
        for key, val in T.E.items():
            if key[1] == x:
                roleToPrint = val
        print(f"+--({roleToPrint})- {T.V[x].name}")
        flag[depth] = False
    else:
        # print(f"+--- {T.V[x].name}")
        roleToPrint = ""
        for key, val in T.E.items():
            if key[1] == x:
                roleToPrint = val
        print(f"+--({roleToPrint})- {T.V[x].name}")

    it = 0
    for node in T.tree[x]:
        it += 1

        #         depth += 1
        depth = vertex_depths[f"{T.vertex_notation}{node}"]
        isLast_arg = it == len(T.tree[x]) - 1

        printNTree(node, flag, depth, isLast_arg, T, vertex_depths)

    flag[depth] = True


def display_tree(T):
    printNTree(x=0, flag=[True for _ in range(len(T.V))], depth=0, isLast=False, T=T, vertex_depths=T.vertex_depths())


def print_isomorphisms(isomorphisms):
    print("isomorphisms = ")
    for key, val in isomorphisms.items():
        print(f"\t{key} -> ", end='')
        for node_left, node_right in val:
            print(f"({node_left.name}{node_right.name})", end='')
        print()


def print_isomorphisms_str(isomorphisms):
    output_str = "isomorphisms = \n"
    for key, val in isomorphisms.items():
        output_str += f"\t{key} -> "
        for node_left, node_right in val:
            output_str += f"({node_left.name}{node_right.name})"
        output_str += "\n"
    return output_str
