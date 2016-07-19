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
        self._act = partial(op.add, 0)

    def eval(self):
        try:
            return self._eval(ast.parse(self.expr, mode='eval').body)
        except:
            return \
                '%s is not a valid arithmetic operation' % (self.expr[:-1])

    def _peek(self, stack):
        if len(stack) > 0:
            return stack[-1]
        return None

    def _eval(self, node):
        # Check for empty tree
        if node is None:
            return

        stack = []

        while(True):

            while node:
                # Push node's right child and then node to stack
                if not isinstance(node, ast.Num):
                    stack.append(node.right)
                stack.append(node)

                # Set node as node's left child
                node = None if isinstance(node, ast.Num) else node.left
            # Pop an item from stack and set it as node
            node = stack.pop()

            # If the popped item has a right child and the
            # right child is not processed yet, then make sure
            # right child is processed before node
            if (not isinstance(node, ast.Num) and
                    self._peek(stack) == node.right):
                # Remove right child from stack
                stack.pop()
                # Push node back to stack
                stack.append(node)
                # change node so that the righ childis processed next
                node = node.right

            # Else print node's data and set node as None
            else:
                if isinstance(node, ast.Num):
                    print '#', node.n
                    self._result = self._act(node.n)
                if isinstance(node, ast.BinOp):
                    print node.op
                    print 'res:', self._result
                    self._act = partial(operators[type(node.op)], self._result)
                elif isinstance(node, ast.UnaryOp):
                    print node.op
                    print 'res:', self._result
                    self.ans.append(node.op)
                # ans.append(node.data)
                node = None

            if (len(stack) <= 0):
                    break
        return self._result

a = '1 + 2 - 3'
evalu = EvalExp(a)
print evalu.eval()
