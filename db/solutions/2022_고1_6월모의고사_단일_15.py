import sympy as sp

x = sp.Symbol('x')
P = -x**2 - x - 3

# 조건 (가) 검증: P(x) ≥ -2x - 3의 해는 0 ≤ x ≤ 1
inequality = P - (-2*x - 3)
inequality_simplified = sp.simplify(inequality)
print(f'P(x) + 2x + 3 = {inequality_simplified}')
# -x(x-1) ≥ 0 ⟺ 0 ≤ x ≤ 1

# 조건 (나) 검증: P(x) = -3x - 2는 중근
eq = P + 3*x + 2
eq_solved = sp.solve(eq, x)
print(f'P(x) = -3x - 2의 해: {eq_solved}')
if len(eq_solved) == 1:
    print(f'중근 O: x = {eq_solved[0]}')

# P(-1) 계산
result = P.subs(x, -1)
print(f'P(-1) = {result}')
if result == -3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')