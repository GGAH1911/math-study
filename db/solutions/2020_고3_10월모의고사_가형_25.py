import sympy as sp
# σ=1, n표본, 95%(z=1.96) CI 폭 b-a=2·1.96/√n. 100(b-a)=49. n?
CANDIDATE = 64
n = sp.symbols('n', positive=True)
nv = sp.solve(100*2*sp.Rational(196,100)/sp.sqrt(n) - 49, n)[0]
print('VERIFY_PASS' if nv == CANDIDATE else 'VERIFY_FAIL')
