from collections import deque


class BipartiteGraph:

    def __init__(self, n: int, m: int):
        # Cardinality of left set:
        self.n = n

        # Cardinality of right set:
        self.m = m

        # 0 := left set, 1 := right set
        self.V: dict[int, list[int]] = {i: [] for i in range(n)}
        self.U: dict[int, list[int]] = {i: [] for i in range(m)}

        # Adjacency map for both sets (V is left, U is right set):
        self.adj: dict[bool, dict[int, list[int]]] = {False: self.V, True: self.U}

        # Rows are vertices of left set, columns are vertices of right set:
        # self.A = [[0 for _ in range(m)] for _ in range(n)]

    def add_edge(self, v: int, w: int):
        # Add a bidirectional edge between v and w:
        self.adj[False][v].append(w)
        self.adj[True][w].append(v)
        # self.A[v][w] = 1
        # self.A[w][v] = 1

    def find_maximal_matchings(self):
        """ My algorithm for finding all maximal matchings for connected bipartite graphs. """
        notation: dict[int, str] = {0: 'v', 1: 'u'}

        # Matchings:
        M: list[list[tuple]] = []

        # Start from the left side:
        Q: deque[tuple] = deque()
        Q.append((False, 0))

        # 0 := left side, 1 := right side:
        visited: dict[bool, set[int]] = {False: {0}, True: set()}

        # Initialize the maximal cardinality:
        max_card: int = 0

        # While there are nodes in the queue:
        while Q:
            # Get the side (left or right set) and next node to evaluate:
            side, current_node = Q.popleft()

            # For every neighbouring vertex of the current node:
            for vertex in self.adj[side][current_node]:

                # If the vertex is not visited:
                if vertex not in visited[not side]:
                    # Add it to the queue wrt to its side:
                    Q.append((not side, vertex))

                    # Add the current node to visited wrt the side:
                    visited[not side].add(vertex)

            if len(M) == 0:
                for vertex in self.adj[side][current_node]:
                    new_matching: list[tuple] = [(f"v{current_node}", f"u{vertex}")]
                    M.append(new_matching)
            else:
                n1: str = notation[1 if side else 0] + str(current_node)

                matchings: list[list[tuple]] = [x for x in M]

                to_remove_idx: set[int] = set()
                i: int = 0

                for matching in matchings:
                    init_check_left: set[str] = set()
                    init_check_right: set[str] = set()

                    check: list[set[str]] = [init_check_left, init_check_right]

                    for x in matching:
                        check[0].add(x[0])
                        check[1].add(x[1])

                    for vertex in self.adj[side][current_node]:
                        n2: str = notation[1 if not side else 0] + str(vertex)

                        if n1 in check[1 if side else 0] or n2 in check[1 if not side else 0]:
                            continue

                        current_matching: list[tuple] = [x for x in M[i]]

                        pair: tuple = (n1, n2) if not side else (n2, n1)

                        current_matching.append(pair)

                        M.append(current_matching)

                        to_remove_idx.add(i)

                    i += 1

                M1: list[list[tuple]] = []
                for k in range(len(M)):
                    if k in to_remove_idx or len(M[k]) < max_card:
                        continue
                    M1.append(M[k])
                    max_card = len(M[k])

                M: list[list[tuple]] = [item for item in M1]

        return M
