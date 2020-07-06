exp1 = ('+', ('*', 2, 3), ('*', 5, 6))
exp2 = ('+', ('+', 1, 2), 3)
exp3 = ('-', ('+', 1, 2), 3)
exp4 = ('*', ('*', ('+', 1, 2), ('+', 3, 4)), ('+', 5, 6))


def compute(token, val1, val2):
    if token == '+':
        return val1 + val2
    elif token == '-':
        return val1 - val2
    elif token == '*':
        return val1 * val2
    elif token == '/':
        return val1 / val2

    return 0


def eval(tree):
    if type(tree) == tuple:
        return compute(tree[0], eval(tree[1]), eval(tree[2]))
    else:
        return tree


def tuple2ExprPrefix(tree):
    if type(tree) == tuple:
        print(tree[0], end='')
        tuple2ExprPrefix(tree[1])
        tuple2ExprPrefix(tree[2])
    else:
        print(tree, end='')


def tuple2ExprInfix(tree, is_root=False):
    is_par = False
    if type(tree) == tuple:
        if tree[0] != '*' and tree[0] != '/' and not is_root:
            is_par = True
        if is_par:
            print(end='(')

        tuple2ExprInfix(tree[1])
        print(tree[0], end='')
        tuple2ExprInfix(tree[2])

        if is_par:
            print(end=')')

    else:
        print(tree, end='')


# print(eval(exp2))
# tuple2ExprPrefix(exp1)
tuple2ExprInfix(exp4, True)
