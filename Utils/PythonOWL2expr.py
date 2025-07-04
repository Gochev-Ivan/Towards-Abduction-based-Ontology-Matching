import re


def remove_outer_parens_per_conjunct(expr: str) -> str:
    def is_property_start(s):
        s = s.lstrip()
        while s.startswith('('):
            s = s[1:].lstrip()
        first_word = re.match(r'[^\s()]+', s)
        return first_word and "some" in s

    def strip_outer_parens(s):
        s = s.strip()
        if s[1] == '(' and s[-2] == ')':
            return s[1:-1]
        if not s.startswith('(') or not s.endswith(')'):
            return s
        if is_property_start(s):
            return s
        depth = 0
        for i, char in enumerate(s):
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                if depth == 0 and i != len(s) - 1:
                    return s
        return s[1:-1]

    def split_by_top_level_and(s):
        parts = []
        current = ''
        depth = 0
        i = 0
        while i < len(s):
            if s[i] == '(':
                depth += 1
            elif s[i] == ')':
                depth -= 1
            if depth == 0 and s[i:i+5] == ' and ':
                parts.append(current.strip())
                current = ''
                i += 5
                continue
            current += s[i]
            i += 1
        if current:
            parts.append(current.strip())
        return parts

    conjuncts = split_by_top_level_and(expr)
    stripped = [strip_outer_parens(c) for c in conjuncts]
    return ' and '.join(stripped)


def strip_prefixes(expression):
    expression = expression.replace('owl.Thing', 'T')
    return re.sub(r'\b[\w\-]+\.', '', expression)


def replace_logical_operators(expression):
    expression = expression.replace('&', 'and')
    expression = expression.replace('|', 'or')
    return expression


def find_balanced_subexpr(expr, start_index):
    if expr[start_index] != '(':
        raise ValueError("Expected '(' at start_index")
    depth = 1
    for i in range(start_index + 1, len(expr)):
        if expr[i] == '(':
            depth += 1
        elif expr[i] == ')':
            depth -= 1
            if depth == 0:
                return expr[start_index + 1:i], i
    raise ValueError("Unbalanced parentheses")


def parse_restrictions(expression):
    pattern = re.compile(r'(\w+)\.(some|only|value|min|max|exactly)\(')
    i = 0
    result = ''
    while i < len(expression):
        match = pattern.search(expression, i)
        if not match:
            result += expression[i:]
            break
        result += expression[i:match.start()]
        prop, restriction = match.group(1), match.group(2)
        subexpr, end_index = find_balanced_subexpr(expression, match.end() - 1)
        transformed_subexpr = transform_owl_expression(subexpr)
        result += f'({prop} {restriction} ({transformed_subexpr}))'
        i = end_index + 1
    return result


def normalize_whitespace(expression):
    return ' '.join(expression.strip().split())


def transform_owl_expression(expression):
    expression = parse_restrictions(expression)
    expression = normalize_whitespace(expression)
    expression = replace_logical_operators(expression)
    expression = strip_prefixes(expression)
    return expression


def POWL2expr(expression):
    expression = transform_owl_expression(expression)
    expression = remove_outer_parens_per_conjunct(expression)
    return expression
