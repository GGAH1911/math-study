import sympy as sp
from sympy import symbols, limit, oo, simplify

a, d, n = symbols('a d n', real=True)
a_n = a + (n-1)*d
a_n1 = a + n*d
a_n2 = a + (n+1)*d

b_n = -a_n2 / a_n
limit_value = limit(b_n, n, oo)

verification = simplify(a_n - 2*a_n1 + a_n2)

if verification == 0 and limit_value == -1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')