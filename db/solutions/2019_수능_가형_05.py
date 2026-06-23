from sympy import *
x, m_sym = symbols('x m')
# Graph A translated by m
graph_A = 2**(x - m_sym) + 2
# Inverse of graph A: solve y = 2^(x-m)+2 for x, then swap
y_sym = symbols('y')
inv_expr = solve(Eq(y_sym, graph_A), x)[0]  # x = log2(y-2) + m
# Substitute x->x, y->y (swap x,y to get inverse function)
inv_func = inv_expr.subs(y_sym, x)  # y = log2(x-2) + m
# Graph B: log2(8*(x-2))
graph_B = log(8*(x-2), 2)
graph_B_simplified = simplify(graph_B)
# For symmetry wrt y=x: inverse of A == graph B
# log2(x-2) + m = 3 + log2(x-2)  => m = 3
m_val = solve(Eq(inv_func, graph_B_simplified), m_sym)
if len(m_val) == 1 and m_val[0] == 3:
    print('VERIFY_PASS')
else:
    # try numeric approach
    diff = simplify(inv_func.subs(m_sym, 3) - graph_B_simplified)
    if diff == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL', m_val)
