# a1=2, a_{n+1}=a_n/n+4 → a3?  점화식을 그대로 돌린다.
CANDIDATE = 7
import sympy as sp

a = {1: sp.Integer(2)}
for n in (1, 2):
    a[n+1] = sp.simplify(sp.Rational(1, n)*a[n] + 4)
print('VERIFY_PASS' if sp.simplify(a[3] - CANDIDATE) == 0 else 'VERIFY_FAIL')
