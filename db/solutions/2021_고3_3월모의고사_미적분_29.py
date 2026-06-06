import sympy as sp
import numpy as np

n = sp.Symbol('n', positive=True, integer=True)

# 원의 중심
h = (1 + n**2)/(1 + 4*n)
k = (4*n + 2*n**2 + 12*n**3)/(1 + 4*n)

# a_n
a_n = k/h
a_n_simplified = sp.simplify(a_n)
print(f'a_n = {a_n_simplified}')

# 극한
limit = sp.limit(a_n/n, n, sp.oo)
print(f'lim(n→∞) a_n/n = {limit}')

if limit == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')