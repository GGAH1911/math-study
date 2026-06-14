from sympy import symbols, limit, Piecewise
a = symbols('a')
x = symbols('x')

# x ≠ 1일 때 f(x) = ax + 3, x = 1일 때 f(x) = 5
f = Piecewise((a*x + 3, x != 1), (5, True))

# x=1에서 연속이려면 lim f(x) = f(1)이어야 함
lim_val = limit(a*x + 3, x, 1)  # x → 1일 때 ax + 3의 극한
f_at_1 = 5

# a를 구함
from sympy import solve
a_value = solve(lim_val - f_at_1, a)[0]

if a_value == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')