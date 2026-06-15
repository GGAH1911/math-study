import sympy as sp
from functools import lru_cache

a1 = sp.symbols('a1')

@lru_cache(maxsize=None)
def a(n):
    if n == 1:
        return a1
    if n % 2 == 0:
        return a(n // 2) - 1
    return 2 * a((n - 1) // 2) + 1

# a_20 = 1 조건으로 a1 결정
sol = sp.solve(sp.Eq(sp.expand(a(20)), 1), a1)
assert len(sol) == 1, 'a1 not unique'
a1_val = sol[0]

# 조건 재확인 및 합 계산
check20 = sp.simplify(a(20).subs(a1, a1_val))
S = sp.nsimplify(sum(sp.expand(a(n)).subs(a1, a1_val) for n in range(1, 64)))

if check20 == 1 and sp.simplify(S - 728) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
