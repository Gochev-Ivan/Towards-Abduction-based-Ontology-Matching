import pandas as pd
from tabulate import tabulate


class DTNode:

    def __init__(self, name, idx, label):
        self.name = name
        self.idx = idx
        self.label = label


class DescriptionTree:

    def __init__(self, vertex_notation='v'):
        self.vertex_notation = vertex_notation
        self.tree = {}
        self.V = {}
        self.E = {}

    def get_parent(self, vertex):
        for parent, children in self.tree.items():
            if vertex in children:
                return parent

    def deg(self):
        return {vertex: len(children) for vertex, children in self.tree.items()}

    def Sr(self):
        return set(self.E.values())

    def jaccard_vec(self, subtree_root, signature_roles=None, depth=-1):
        if signature_roles is None:
            signature_roles = self.E.values()

        prune = False if depth == -1 else True

        visited = set()
        vector = pd.Series(0, index=signature_roles)
        for parent, val in self.tree.items():
            if subtree_root in val:
                vector[self.E[(parent, subtree_root)]] += 1
        for path in self.find_all_complete_paths_dfs(root=subtree_root):
            if prune:
                path = path[:depth + 1]
            for e in zip(path[:len(path)], path[1:]):
                if e not in visited:
                    vector[self.E[e]] += 1
                    visited.add(e)
        return vector

    def deg_vec(self, path):
        degrees = self.deg()
        return [degrees[vertex] for vertex in path]

    def role_vec(self, path):
        return [self.E[e] for e in zip(path[:len(path)], path[1:])] + [1]

    def L(self, subtree_root=0, depth=-1):
        prune = False if depth == -1 else True

        degrees = self.deg()

        A = [[0 for _ in range(len(self.V))] for _ in range(len(self.V))]
        for e in self.E:
            A[e[0]][e[1]] = 1

        for i in range(len(degrees)):
            A[i][i] = degrees[i]

        Sv = []
        Se = []

        for path in self.find_all_complete_paths_dfs(root=subtree_root):
            if prune:
                path = path[:depth + 1]
            for e in zip(path[:len(path)], path[1:]):
                if e not in Se:
                    Se.append(e)
                if e[0] not in Sv:
                    Sv.append(e[0])
                if e[1] not in Sv:
                    Sv.append(e[1])

        if subtree_root not in Sv:
            Sv.append(subtree_root)

        L = [[0 for _ in range(len(Sv))] for _ in range(len(Sv))]

        x = 0
        for v in Sv:
            y = 0
            for u in Sv:
                L[x][y] = A[v][u]
                y += 1
            x += 1

        return L

    def vertex_depths(self):
        # Initialize the Vm and En variables:
        Vm = {node.name: vertex_idx for vertex_idx, node in self.V.items()}

        En = self.E.keys()

        # Initialize the depths variable:
        # Initialize the depth of the root:
        depths = {f"{self.vertex_notation}0": 0}

        # Get the reversed mapping of vertices:
        Vm_reversed = {val: key for key, val in Vm.items()}

        # Iterate over all edges and get all nodes to define their depths:
        for n1, n2 in sorted(list(En)):
            # Construct the vertices:
            vertex1 = Vm_reversed[n1]
            vertex2 = Vm_reversed[n2]

            # Define the depth of the vertex:
            depths[vertex2] = depths[vertex1] + 1

        # Return the depths
        return depths

    def add_vertex(self, vertex, label):
        if vertex not in self.tree:
            self.tree[vertex] = []
            self.V[vertex] = DTNode(f"{self.vertex_notation}{vertex}", vertex, label=label)

    def update_vertex_label(self, vertex, label):
        if vertex in self.tree:
            self.V[vertex].label += label

    def add_edge(self, v, u, edge_label):
        if v not in self.tree:
            raise ValueError(f"The node {v} is not in the tree.")

        if u not in self.tree:
            raise ValueError(f"The node {u} is not in the tree.")

        if u not in self.tree[v]:
            self.tree[v].append(u)

        if (v, u) not in self.E:
            self.E[(v, u)] = edge_label

    def find_all_complete_paths_dfs(self, root):
        def dfs(current, path):
            if not self.tree.get(current):
                all_paths.append(path)
                return
            for neighbor in self.tree[current]:
                if neighbor not in path:
                    dfs(neighbor, path + [neighbor])

        if root not in self.tree:
            return []

        all_paths = []
        dfs(root, [root])
        return all_paths

    def tree2expr(self, root):
        if len(self.E) == 0:
            return " and ".join(self.V[0].label)

        def dfs(current, path, cnt):
            if not self.tree.get(current):
                all_paths.append(path)
                final_label.append(f"{'))'}")
                final_label.append(" and ")
                return
            for neighbor in self.tree[current]:
                if neighbor not in path:
                    final_label.append(f"({self.E[(path[-1], neighbor)]} some ({' and '.join(self.V[neighbor].label)}")
                    dfs(neighbor, path + [neighbor], cnt + 2)
            final_label[-1] = f"{'))'}"
            final_label.append(" and ")

        if root not in self.tree:
            return []

        all_paths = []
        root_label = self.V[root].label
        if '' in root_label:
            root_label.remove('')

        final_label = [f"{' and '.join(root_label)} and "]
        dfs(root, [root], 0)
        final_label = "".join(final_label)
        final_label = final_label[:len(final_label) - 7]
        return final_label

    def display(self):
        df = pd.DataFrame(columns=['V', 'E'])
        V_column, E_column = "", ""

        for v in self.tree:
            edges = ', '.join([f"{self.V[u].name}{self.V[u].label}" for u in self.tree[v]])
            V_column += f"{self.V[v].name}{self.V[v].label} -> {edges}\n"
        for edge, role in self.E.items():
            E_column += f"{edge[0]} -- {role} --> {edge[1]}\n"

        df.loc[len(df)] = [V_column, E_column]
        print(tabulate(df, headers='keys', tablefmt='psql'))

    def display_str(self):
        df = pd.DataFrame(columns=['V', 'E'])
        V_column, E_column = "", ""

        for v in self.tree:
            edges = ', '.join([f"{self.V[u].name}{self.V[u].label}" for u in self.tree[v]])
            V_column += f"{self.V[v].name}{self.V[v].label} -> {edges}\n"
        for edge, role in self.E.items():
            E_column += f"{edge[0]} -- {role} --> {edge[1]}\n"

        df.loc[len(df)] = [V_column, E_column]
        return tabulate(df, headers='keys', tablefmt='psql')
