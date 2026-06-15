import sympy as sp

# 2020 9월모평 나형 23: f가 x=2에서 연속, 좌극한 a+2, 우극한 3a-2. a+f(2)?
# 연속 ⟹ a+2 = 3a-2 = f(2)
CANDIDATE = 6
a = sp.symbols('a')
av = sp.solve((a + 2) - (3 * a - 2), a)[0]   # a = 2
f2 = 3 * av - 2                               # f(2) = 우극한
print('VERIFY_PASS' if av + f2 == CANDIDATE else 'VERIFY_FAIL')
