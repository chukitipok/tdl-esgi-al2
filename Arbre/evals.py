names = {}
functions = {}
return_value = None


class Function:
    def __init__(self, name, args, body, is_void):
        self.name = name
        self.args = args
        self.body = body
        self.is_void = is_void

    def __str__(self):
        return f"name: {self.name}"


def evalInst(tree):
    global return_value

    if tree == 'Empty':
        return

    if tree[0] == 'Program':
        evalInst(tree[1])

    if tree[0] == 'Print':
        print(evalExpr(tree[1]))

    if tree[0] == 'Affect':
        names[tree[1]] = evalExpr(tree[2])

    if tree[0] == 'Block':
        for i in range(1, len(tree)):
            evalInst(tree[i])

    if tree[0] == 'Inst':
        evalInst(tree[1])

    if tree[0] == 'If':
        if evalExpr(tree[1]):
            evalInst(tree[2])

    if tree[0] == 'If Else':
        if evalExpr(tree[1]):
            evalInst(tree[2])
        else:
            evalInst(tree[3])

    if tree[0] == 'For':
        evalInst(tree[1])
        while evalExpr(tree[2]):
            evalInst(tree[4])
            evalInst(tree[3])

    if tree[0] == 'While':
        while evalExpr(tree[1]):
            evalInst(tree[2])

    if tree[0] == 'Return':
        return_value = evalExpr(tree[1])

    if tree[0] == 'Function':
        functions[tree[1]] = Function(tree[1], tree[2], tree[3], tree[4])

    if tree[0] == 'Call':
        f = functions[tree[1]]

        for i in range(1, len(tree[2])):
            names[f.args[i]] = evalExpr(tree[2][i])

        evalInst(f.body)

        if return_value is not None:
            evalExpr(return_value)

    if tree[0] == 'Arg':
        for i in range(1, len(tree)):
            evalExpr(tree[i])

    if tree[0] == 'Param':
        for i in range(1, len(tree)):
            evalExpr(tree[i])


def evalExpr(tree):
    if type(tree) == int:
        return tree
    if type(tree) == str:
        return names[tree]
    if tree[0] == '+':
        return evalExpr(tree[1]) + evalExpr(tree[2])
    if tree[0] == '-':
        return evalExpr(tree[1]) - evalExpr(tree[2])
    if tree[0] == '*':
        return evalExpr(tree[1]) * evalExpr(tree[2])
    if tree[0] == '/':
        return evalExpr(tree[1]) / evalExpr(tree[2])
    if tree[0] == '<=':
        return evalExpr(tree[1]) <= evalExpr(tree[2])
    if tree[0] == '>=':
        return evalExpr(tree[1]) >= evalExpr(tree[2])
    if tree[0] == '<':
        return evalExpr(tree[1]) < evalExpr(tree[2])
    if tree[0] == '>':
        return evalExpr(tree[1]) > evalExpr(tree[2])
    if tree[0] == '==':
        return evalExpr(tree[1]) == evalExpr(tree[2])
    if tree[0] == '!=':
        return evalExpr(tree[1]) != evalExpr(tree[2])
