from op_evalv2 import EvalExp
from op_eval import eval_expr
import time


def compare(op):
    ticks = time.time()
    it = EvalExp(op).eval()
    print 'Iterative: ', time.time() - ticks
    ticks = time.time()
    re = eval_expr(op)
    print 'Recursive: ', time.time() - ticks
    assert it, re


op = '20 - 55 - 20 + 100 + 80 + 23 * 2 * (2 + 4) - 4 + 3 / 3 - 2 * 5 + 1 - 2 / (2 * 3 + 1 + 2 - 3 + 2 + 1) * 3 / 4 + 1 + 2 + 3 + 1 + 2 + 3 + 3 * 4324 + 32 - 3423 * 34234 - 43243 + 3423 - 43242 + 43 + 3242 -3242 * 324234 *342*234234-43234*342*42-34-34-24*2*4-234-2-42-4*2*42-34*23*-42*4*234*23-4'
compare(op)
print '################'
op = '20 - 55 - 20 + 100 + 80 + 23 * 2 * (2 + 4) - 4 + 3 / 3 - 2 * 5 + 1 - 2 / (2 * 3 + 1 + 2 - 3 + 2 + 1) * 3 / 4 + 1 + 2 + 3 + 1 + 2 + 3 + 3 * 4324 + 32 - 3423 * 34234 - 43243 + 3423 - 43242 + 43 + 3242 -3242 * 324234 *342*234234'
compare(op)
print '################'
op = '20 - 55 - 20'
compare(op)
print '################'
