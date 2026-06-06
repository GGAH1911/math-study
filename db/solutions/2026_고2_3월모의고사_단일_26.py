import sympy as sp
k = sp.Symbol('k', real=True)
a, b = 3, -12
f = lambda x: a*(x-2)**2 + b

# 조건 확인: 최댓값이 3k^4 + 12k^2
f_left = f(-k**2)
expected = 3*k**4 + 12*k**2
if sp.simplify(f_left - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')