import sympy as sp

# 2020 수능 나형 24: X ~ B(80,p), E(X)=20. V(X)? (가형 23과 동일)
CANDIDATE = 15
p = sp.symbols('p', positive=True)
n = 80
pv = sp.solve(n * p - 20, p)[0]
V = n * pv * (1 - pv)
print('VERIFY_PASS' if V == CANDIDATE else 'VERIFY_FAIL')
