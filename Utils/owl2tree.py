from collections import deque
from Graphs.DescriptionTree import DescriptionTree
import re


def signature(expression: str):
    tokens = re.findall(r'\w+|[()]', expression)
    classes = set()
    properties = set()

    def parse(tokens):
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == 'some' or token == 'only':
                if i > 0 and re.match(r'\w+', tokens[i - 1]):
                    properties.add(tokens[i - 1])
                i += 1
            elif token == '(':
                depth = 1
                j = i + 1
                while j < len(tokens) and depth > 0:
                    if tokens[j] == '(':
                        depth += 1
                    elif tokens[j] == ')':
                        depth -= 1
                    j += 1
                subexpr = tokens[i + 1:j - 1]
                parse(subexpr)
                i = j - 1
            elif re.match(r'\w+', token):
                if i + 1 < len(tokens) and tokens[i + 1] in ('some', 'only'):
                    pass
                elif i == 0 or tokens[i - 1] not in ('some', 'only'):
                    classes.add(token)
            i += 1
    parse(tokens)
    if 'and' in classes:
        classes.remove('and')
    if 'SubClassOf' in classes:
        classes.remove('SubClassOf')
    return classes, properties


def getConjuncts(C):
    x = 0
    p = 0
    start_idx = 0
    result = []
    while x < len(C):
        if (C[x] == "(") and (p == 0):
            start_idx = x
        if C[x] == "(":
            p += 1
        if C[x] == ")":
            p -= 1
        if (C[x] == ")") and (p == 0):
            end_idx = x
            result.append(C[start_idx + 1:end_idx])
        x += 1
    return result


def getExpressionParts(result):
    expressionConj = []
    for expr in result:
        temp = []
        if "(" not in expr:
            temp.append(expr)
            expressionConj.append(temp)
            continue
        for x in range(len(expr)):
            character = expr[x]
            if character == "(":
                temp.append(expr[0:x - 1])
                temp.append(expr[x + 1:len(expr) - 1])
        expressionConj.append(temp)
    return expressionConj


def getTopLevelConjuncts(C):
    conjuncts = getConjuncts(C)
    exp = C
    for e in conjuncts:
        exp = exp.replace(e, "")
    conj = [*set(exp.split(" and "))]
    if "()" in conj:
        conj.remove("()")
    return conj


def expr2tree(C, inputted_vertex_notation='v'):
    T = DescriptionTree(inputted_vertex_notation)
    if "some" not in C:
        T.add_vertex(0, C.split(" and "))
        return T
    queue = deque()
    index_v, index_u = 0, 1
    queue.append((C, index_v))
    while queue:
        pair = queue.popleft()
        current_C = pair[0]
        idx_v = pair[1]
        result = getConjuncts(current_C)
        expressionParts = getExpressionParts(result)
        newExpressionParts = []
        for part in expressionParts:
            newPart = []
            newPart.insert(0, part[0])
            for part_idx in range(1, len(part)):
                if ("some" in part[part_idx]) and ("and" not in part[part_idx]):
                    newPart.insert(part_idx, "T and (" + part[part_idx] + ")")
                else:
                    newPart.append(part[part_idx])
            newExpressionParts.append(newPart)
        for part in newExpressionParts:
            edge_label = ""
            concept_labels = ""
            if len(part) == 1:
                arr = part[0].split(" some ")
                edge_label = arr[0]
                concept_labels = arr[1]
            else:
                for x in range(len(part[0])):
                    if part[0][x] == " ":
                        break
                    edge_label += part[0][x]
                for x in range(len(part[1])):
                    if part[1][x] == "(":
                        break
                    concept_labels += part[1][x]
            arr = concept_labels.split(" and ")
            label_v = getTopLevelConjuncts(current_C)
            label_u = []
            for x in range(len(arr)):
                label_u.append(arr[x])
            T.add_vertex(vertex=idx_v, label=label_v)
            T.add_vertex(vertex=index_u, label=label_u)
            T.add_edge(idx_v, index_u, edge_label)
            if len(part) != 1:
                if len(part[1]) != 0:
                    queue.append((part[1], index_u))
            index_u += 1
    return T
