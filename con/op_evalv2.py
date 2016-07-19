import ast
import operator as op
from functools import partial


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
        # Set current to node of binary tree
        current = node
        s = []  # initialze stack
        done = 0
        act = partial(op.add, 0)
        res = 0

        while(not done):

            # Reach the left most Node of the current Node
            if current is not None:

                # Place pointer to a tree node on the stack
                # before traversing the node's left subtree
                s.append(current)
                current = \
                    current.left if not isinstance(current, ast.Num) else None

            # BackTrack from the empty subtree and visit the Node
            # at the top of the stack; however, if the stack is
            # empty you are done
            else:
                if len(s) > 0:
                    current = s.pop()
                    if isinstance(current, ast.Num):
                        res = act(current.n)
                    if isinstance(current, ast.BinOp):
                        act = \
                            partial(operators[type(current.op)], res)
                    elif isinstance(current, ast.UnaryOp):
                        act = \
                            partial(operators[type(current.op)], res)
                    # We have visited the node and its left
                    # subtree. Now, it's right subtree's turn
                    if not isinstance(current, ast.Num):
                        current = current.right
                    else:
                        current = None
                else:
                    done = 1
        return res
