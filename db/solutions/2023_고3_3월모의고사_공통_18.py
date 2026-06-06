import sympy as sp
n = sp.Symbol('n')
alpha = 4*n
beta = n
term = (1 - alpha) * (1 - beta)
term_simplified = sp.expand(term)
result = sum(term_simplified.subs(n, i) for i in range(1, 8))
if result == 427:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')