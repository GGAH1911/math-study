import sympy as sp
from sympy import symbols, solve, Rational

t = symbols('t', positive=True, real=True)

# S1 = t^3
S1 = t**3

# 경우 1: 0 < t < 2
S2_case1 = t * (2*t - t**2)  # |t^2 - 2t| = 2t - t^2
ratio1 = S1 / S2_case1
eq1 = ratio1 - 5
t1_sol = solve(eq1, t)
t1_valid = [sol for sol in t1_sol if sol > 0 and sol < 2]

# 경우 2: t > 2
S2_case2 = t * (t**2 - 2*t)  # |t^2 - 2t| = t^2 - 2t
ratio2 = S1 / S2_case2
eq2 = ratio2 - 5
t2_sol = solve(eq2, t)
t2_valid = [sol for sol in t2_sol if sol > 2]

# 모든 유효한 t 값
all_t = t1_valid + t2_valid
total = sum(all_t)

# 검증
for t_val in all_t:
    S1_val = t_val**3
    S2_val = t_val * abs(t_val**2 - 2*t_val)
    ratio = S1_val / S2_val
    assert abs(ratio - 5) < 1e-10, f'Ratio check failed for t={t_val}'

if total == Rational(25, 6):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')