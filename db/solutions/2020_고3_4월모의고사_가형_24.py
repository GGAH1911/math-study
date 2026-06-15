import sympy as sp
# f(x)=2^(x+p)+q, 점근선 y=-4 → q=-4, f(0)=0. f(4)?
CANDIDATE = 60
p = sp.symbols('p', real=True)
q = -4
pv = sp.solve(2**p + q, p)[0]      # 2^p-4=0 → p=2
f = lambda x: 2**(x+pv) + q
print('VERIFY_PASS' if f(4) == CANDIDATE else 'VERIFY_FAIL')
