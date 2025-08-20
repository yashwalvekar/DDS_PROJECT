import math

# Operators: precedence (higher = tighter), associativity ('L' or 'R'), arity
OPS = {
    '+': (1, 'L', 2),
    '-': (1, 'L', 2),
    '*': (2, 'L', 2),
    '/': (2, 'L', 2),
    '^': (3, 'R', 2),
    'u-': (4, 'R', 1),  # unary minus
}

def is_number(tok: str) -> bool:
    try:
        float(tok)
        return True
    except ValueError:
        return False

def tokenize(expr: str):
    tokens = []
    i, n = 0, len(expr)
    prev = None  # previous token (to detect unary minus)
    while i < n:
        ch = expr[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit() or ch == '.':
            j = i + 1
            dot_seen = (ch == '.')
            while j < n and (expr[j].isdigit() or (expr[j] == '.' and not dot_seen)):
                if expr[j] == '.':
                    dot_seen = True
                j += 1
            tokens.append(expr[i:j])
            prev = tokens[-1]
            i = j
            continue

        if ch in '+-*/^()':
            if ch == '-':
                # unary if at start or after another operator or '('
                if prev is None or (prev in OPS or prev == '('):
                    tokens.append('u-')
                else:
                    tokens.append('-')
            else:
                tokens.append(ch)
            prev = tokens[-1]
            i += 1
            continue

        raise ValueError(f"Invalid character: {ch!r}")
    return tokens

def infix_to_postfix(tokens):
    out = []
    stack = []
    for tok in tokens:
        if is_number(tok):
            out.append(tok)
        elif tok in OPS:
            p_tok, assoc_tok, _ = OPS[tok]
            while stack and stack[-1] in OPS:
                p_top, assoc_top, _ = OPS[stack[-1]]
                if (p_top > p_tok) or (p_top == p_tok and assoc_tok == 'L'):
                    out.append(stack.pop())
                else:
                    break
            stack.append(tok)
        elif tok == '(':
            stack.append(tok)
        elif tok == ')':
            while stack and stack[-1] != '(':
                out.append(stack.pop())
            if not stack or stack[-1] != '(':
                raise ValueError("Mismatched parentheses")
            stack.pop()  # remove '('
        else:
            raise ValueError(f"Unknown token: {tok}")
    while stack:
        top = stack.pop()
        if top in ('(', ')'):
            raise ValueError("Mismatched parentheses")
        out.append(top)
    return out

def eval_postfix(postfix):
    st = []
    for tok in postfix:
        if is_number(tok):
            st.append(float(tok))
        elif tok in OPS:
            prec, assoc, arity = OPS[tok]
            if len(st) < arity:
                raise ValueError("Insufficient operands")
            if arity == 1:
                x = st.pop()
                if tok == 'u-':
                    st.append(-x)
                else:
                    raise ValueError(f"Unsupported unary op {tok}")
            elif arity == 2:
                b = st.pop()
                a = st.pop()
                if tok == '+':
                    st.append(a + b)
                elif tok == '-':
                    st.append(a - b)
                elif tok == '*':
                    st.append(a * b)
                elif tok == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    st.append(a / b)
                elif tok == '^':
                    st.append(a ** b)
                else:
                    raise ValueError(f"Unsupported operator {tok}")
        else:
            raise ValueError(f"Unknown token in postfix: {tok}")
    if len(st) != 1:
        raise ValueError("Malformed expression")
    return st[0]

def evaluate(expression: str):
    tokens = tokenize(expression)
    postfix = infix_to_postfix(tokens)
    return eval_postfix(postfix)

if __name__ == "__main__":
    try:
        expr = input("Enter expression: ").strip()
        result = evaluate(expr)
        print("Postfix:", " ".join(infix_to_postfix(tokenize(expr))))
        print("Result:", result)
    except Exception as e:
        print("Error:", e)
