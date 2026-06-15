import sympy as sp
# lim n²a_n=3, lim b_n/n=5. lim n a_n(b_n+2n)? (극한은 주항만 의존)
CANDIDATE = 21
n = sp.symbols('n', positive=True)
a, b = 3/n**2, 5*n
print('VERIFY_PASS' if sp.limit(n*a*(b + 2*n), n, sp.oo) == CANDIDATE else 'VERIFY_FAIL')
