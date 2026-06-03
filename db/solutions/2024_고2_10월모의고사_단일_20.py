import sympy as sp
from sympy import symbols, solve, simplify

# ㄱ 검증: a=1일 때 g(1)=-1
a_val = 1
f_0 = a_val  # f(0) = a
g_1 = (0 - f_0) / 1  # f(1)=0 (1<=1<2 구간)
assert g_1 == -1, f'ㄱ 검증 실패: g(1)={g_1}'

# ㄷ 검증: a=-3/2일 때 y=f(x)와 y=-3/2의 교점
a_val = -3/2
x = symbols('x', real=True)

# x < 1 구간에서 (x-1)(x-a) = -3/2
f_expr = (x - 1) * (x - a_val)
equation = f_expr + 3/2  # (x-1)(x+3/2) + 3/2 = 0
solutions = solve(equation, x)
print(f'x<1에서 f(x)=-3/2의 해: {solutions}')
assert len(solutions) == 2, f'ㄷ 검증 실패: 교점 개수={len(solutions)}'
for sol in solutions:
    assert sol < 1, f'해 {sol}이 범위 x<1을 벗어남'

# 1<=x<2에서 f(x)=0이므로 -3/2와 만나지 않음
# x>=2에서 f(x)=1이므로 -3/2와 만나지 않음

print('VERIFY_PASS')