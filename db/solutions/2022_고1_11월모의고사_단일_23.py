import sympy as sp
x, k = sp.symbols('x k')
# 원래 문제: 이차함수와 직선의 교점
eq = x**2 + 4*x + k + 2*x - 1
eq_simplified = x**2 + 6*x + (k-1)
k_val = 9
disc = 36 - 4*(k_val - 1)
if disc > 0:
    roots = sp.solve(eq_simplified.subs(k, k_val), x)
    if len(roots) == 2 and roots[0] != roots[1]:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')