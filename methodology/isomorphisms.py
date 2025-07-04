import pandas as pd
from numpy import sqrt

from Graphs.BipartiteGraph import *


def jaccard_index(j1, j2, Sr):
    return sum(min(j1[role], j2[role]) for role in Sr) / sum(max(j1[role], j2[role]) for role in Sr)


def f(r, s):
    k = 0
    for i in range(min(len(r), len(s))):
        if r[i] != s[i]:
            break
        k += 1
    return k


def role_sim(r, s, k):
    if r[0] != s[0]:
        return 0

    if r == s:
        return 1

    return k / (max(len(r), len(s)) - 1)


def magnitude_sim(c, d, k):
    return sqrt(sum((c[i] - d[i]) ** 2 for i in range(k))) + (len(c) + len(d) - (2 * k))


def Frobenius_norm(A):
    return sqrt(sum([A[i][j] ** 2 for i in range(len(A)) for j in range(len(A[i]))]))


def filter_queue(queue: dict[tuple, list[list]]):
    f1: dict[tuple[int], list[list]] = {}
    min_heuristics: dict[tuple[int], float] = {}
    for path_1, paths_2 in queue.items():
        path_1 = list(path_1)
        for path_2 in paths_2:
            path1_size: int = len(path_1)
            path2_size: int = len(path_2[0])
            if tuple(path_2[0]) not in f1:
                t: list[list] = []
                if path2_size < path1_size:
                    p_temp: list[int] = path_1[:path2_size]
                    if [p_temp, path_2[1]] not in t:
                        t.append([p_temp, path_2[1]])
                else:
                    if [path_1, path_2[1]] not in t:
                        t.append([path_1, path_2[1]])
                f1[tuple(path_2[0])] = t
                min_heuristics[tuple(path_2[0])] = path_2[1]
            else:
                t: list[list] = []
                if path_2[1] <= min_heuristics[tuple(path_2[0])]:
                    for el in f1[tuple(path_2[0])]:
                        if el[1] == min_heuristics[tuple(path_2[0])]:
                            if path2_size < len(el[0]):
                                p_temp: list[int] = el[0][:path2_size]
                                if [p_temp, el[1]] not in t:
                                    t.append([p_temp, el[1]])
                            else:
                                if el not in t:
                                    t.append(el)
                    if path2_size < path1_size:
                        p_temp: list[int] = path_1[:path2_size]
                        if [p_temp, path_2[1]] not in t:
                            t.append([p_temp, path_2[1]])
                    else:
                        if [path_1, path_2[1]] not in t:
                            t.append([path_1, path_2[1]])
                    f1[tuple(path_2[0])] = t
                    min_heuristics[tuple(path_2[0])] = path_2[1]
    return f1


class Isomorphisms:

    def __init__(self, T1, T2):
        self.T1 = T1
        self.T2 = T2

    def construct_hypotheses(self, rel="SubClassOf"):
        isomorphisms, _ = self.heuristics_subtree_isomorphisms()

        hypotheses = []

        for _, isomorphism in isomorphisms.items():
            L1 = {}
            L2 = {}
            to_contract_1 = set()
            to_contract_2 = set()
            for v, w in isomorphism:
                L1[v.idx] = [item for item in self.T1.V[v.idx].label if item != '']
                L2[w.idx] = [item for item in self.T2.V[w.idx].label if item != '']
                to_contract_1.add(v.idx)
                to_contract_2.add(w.idx)
            to_contract_1 = set(self.T1.V).difference(to_contract_1)
            to_contract_2 = set(self.T2.V).difference(to_contract_2)

            for vertex in to_contract_1:
                parent = self.T1.get_parent(vertex)
                if len(self.T1.tree[vertex]) == 0:
                    label = f"({self.T1.E[(parent, vertex)]} some ({' and '.join(self.T1.V[vertex].label)}))"
                else:
                    label = f"({self.T1.E[(parent, vertex)]} some ({self.T1.tree2expr(vertex)}))"
                if parent not in L1:
                    L1[parent] = [label]
                else:
                    L1[parent].append(label)

            for vertex in to_contract_2:
                parent = self.T2.get_parent(vertex)
                if len(self.T2.tree[vertex]) == 0:
                    label = f"({self.T2.E[(parent, vertex)]} some ({' and '.join(self.T2.V[vertex].label)}))"
                else:
                    label = f"({self.T2.E[(parent, vertex)]} some ({self.T2.tree2expr(vertex)}))"
                if parent not in L2:
                    L2[parent] = [label]
                else:
                    L2[parent].append(label)

            hypothesis = [f"{' and '.join(L1[v.idx])} {rel} {' and '.join(L2[w.idx])}" for v, w in isomorphism]
            hypotheses.append(hypothesis)

        return hypotheses

    def heuristics_subtree_isomorphisms(self):

        df = pd.DataFrame(columns=['path 1', 'path 2',
                                   'jaccard vec 1', 'jaccard vec 2',
                                   'deg_vec 1', 'deg_vec 2',
                                   'role_vec 1', 'role_vec 2',
                                   'k', 'J', 'rho', 'mu', 'Dn', 'h'])

        if len(self.T1.E) == 0 or len(self.T2.E) == 0:
            df.loc[len(df)] = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
            return {0: [(self.T1.V[0], self.T2.V[0])]}, df

        P1 = self.T1.find_all_complete_paths_dfs(root=0)
        P2 = self.T2.find_all_complete_paths_dfs(root=0)

        Sr = [*self.T1.Sr().union(self.T2.Sr())]

        height = lambda paths: max([len(path) for path in paths])
        max_common_depth = min(height(P1), height(P2))

        queue: dict[tuple, list[list]] = {}

        for p1 in P1:
            min_h: float = 0.0
            for p2 in P2:
                p1 = p1[:max_common_depth + 1]
                p2 = p2[:max_common_depth + 1]

                v1 = p1[1]
                w1 = p2[1]

                jaccard_vec1 = self.T1.jaccard_vec(subtree_root=v1, signature_roles=Sr, depth=max_common_depth)
                jaccard_vec2 = self.T2.jaccard_vec(subtree_root=w1, signature_roles=Sr, depth=max_common_depth)

                deg_vec1 = self.T1.deg_vec(path=p1)
                deg_vec2 = self.T2.deg_vec(path=p2)

                role_vec1 = self.T1.role_vec(path=p1)
                role_vec2 = self.T2.role_vec(path=p2)

                J = jaccard_index(j1=jaccard_vec1, j2=jaccard_vec2, Sr=Sr)

                k = f(r=role_vec1, s=role_vec2)

                rho = role_sim(r=role_vec1, s=role_vec2, k=k)

                mu = magnitude_sim(c=deg_vec1, d=deg_vec2, k=k)

                L1 = self.T1.L(subtree_root=v1, depth=max_common_depth)
                L2 = self.T2.L(subtree_root=w1, depth=max_common_depth)
                F1 = Frobenius_norm(L1)
                F2 = Frobenius_norm(L2)
                Dn = (F1 - F2) + abs(len(L1) - len(L2))

                h = (1 / (J ** 2)) * ((mu + Dn) / rho)

                if tuple(p1) not in queue:
                    queue[tuple(p1)] = [[p2, float(h)]]
                    min_h = h
                else:
                    if h <= min_h:
                        queue[tuple(p1)] = [el for el in queue[tuple(p1)] if el[1] == h] + [[p2, float(h)]]
                        min_h = h

                df.loc[len(df)] = [tuple(p1), tuple(p2),
                                   jaccard_vec1, jaccard_vec2, deg_vec1, deg_vec2, role_vec1, role_vec2,
                                   k, J, rho, mu, Dn, h]

        f1: dict[tuple[int], list[list]] = filter_queue(queue=queue)
        n: int = 0
        m: int = 0
        bipartite_graph_edges: list[tuple] = []

        G_V: dict[tuple[int], tuple] = {}
        notation_G_V: dict[str, tuple[int]] = {}
        G_U: dict[tuple[int], tuple] = {}
        notation_G_U: dict[str, tuple[int]] = {}

        mapped_paths_in_all_maximal_solutions: list[tuple] = [(self.T1.V[0], self.T2.V[0])]

        for entry in f1.items():
            path_2 = entry[0]
            if len(entry[1]) == 1:
                path_1: list[int] = entry[1][0][0]
                for path_idx in range(f(self.T1.role_vec(path_1), self.T2.role_vec(path_2))):
                    for pair in zip(path_1[:f(self.T1.role_vec(path_1), self.T2.role_vec(path_2)) + 1],
                                    path_2[:f(self.T1.role_vec(path_1), self.T2.role_vec(path_2)) + 1]):
                        temp_pair = (self.T1.V[pair[0]], self.T2.V[pair[1]])
                        if temp_pair not in mapped_paths_in_all_maximal_solutions:
                            mapped_paths_in_all_maximal_solutions.append(temp_pair)
            else:
                if tuple(path_2) not in G_U:
                    G_U[tuple(path_2)] = (m, f"u{m}")
                    notation_G_U[f"u{m}"] = path_2
                    u_vertex = m
                    m += 1
                else:
                    u_vertex = G_U[tuple(path_2)][0]
                for item in entry[1]:
                    left_path: list[int] = item[0]
                    if tuple(left_path) not in G_V:
                        G_V[tuple(left_path)] = (n, f"v{n}")
                        notation_G_V[f"v{n}"] = tuple(left_path)
                        v_vertex = n
                        n += 1
                    else:
                        v_vertex = G_V[tuple(left_path)][0]
                    bipartite_graph_edges.append((v_vertex, u_vertex))

        G: BipartiteGraph = BipartiteGraph(n, m)
        for edge_pair in bipartite_graph_edges:
            G.add_edge(edge_pair[0], edge_pair[1])

        if len(G_V) == 0 and len(G_U) == 0:
            return {0: mapped_paths_in_all_maximal_solutions}, df

        isomorphisms = {}
        maximal_matchings = G.find_maximal_matchings()
        num_sol: int = 0
        for maximal_solution in maximal_matchings:
            temp_max_sol = []
            for pair_max_sol in maximal_solution:
                T1_path = notation_G_V[pair_max_sol[0]]
                T2_path = notation_G_U[pair_max_sol[1]]
                for paths_idx in range(min(len(T1_path), len(T2_path))):
                    temp_pair = (self.T1.V[T1_path[paths_idx]], self.T2.V[T2_path[paths_idx]])
                    if temp_pair not in temp_max_sol:
                        temp_max_sol.append(temp_pair)
            for mp in mapped_paths_in_all_maximal_solutions:
                if mp not in temp_max_sol:
                    temp_max_sol.append(mp)
            isomorphisms[num_sol] = temp_max_sol
            num_sol += 1

        return isomorphisms, df
