import ast
import operator as op
from functools import partial
import time


# supported operators
operators = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
    ast.USub: op.neg
}


class EvalExp:
    def __init__(self, expr):
        self.expr = expr

    def eval(self):
        try:
            return self._eval(ast.parse(self.expr, mode='eval').body)
        except:
            return '%s is not a valid arithmetic operation' % (self.expr[:-1])

    def _eval(self, node):
        # Base Case
        if node is None:
            return

        res = []
        # create an empty stack and push node to it
        nodeStack = []
        nodeStack.append(node)

        # Note that right child is pushed first so that left
        # is processed first */
        while(len(nodeStack) > 0):

            # Pop the top item from stack and print it
            node = nodeStack.pop()
            res.append(node)
            while (
                len(res) > 1 and
                isinstance(res[-1], ast.Num) and
                isinstance(res[-2], ast.Num)
            ):  # <number>
                n1 = res.pop()
                n2 = res.pop()
                op = res.pop()
                ast_num = ast.Num()
                ast_num.n = operators[type(op.op)](n2.n, n1.n)
                res.append(ast_num)
            # Push right and left children of the popped node
            # to stack
            if isinstance(node, ast.BinOp):
                nodeStack.append(node.right)
                nodeStack.append(node.left)
        return res[0].n

# a = '1 + 2 * 3 - 4 - 2 - 3 * 2 - 3323231232 * 312312 - 32312 / 312312312312312123 * 31231231 - 3123123123 / 3123123 - 2123123123 + 21321312312 * 3123123'
# ticks = time.time()
# print EvalExp(a).eval()
# print time.time() - ticks
