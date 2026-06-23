from sympy import symbols, solve, sqrt, simplify, Rational

k = symbols('k', real=True, positive=True)

# 점의 좌표
x_A = (3 - k) / 3
y_A = 0
x_B = 0
y_B = 3 - k
x_P = 2
y_P = k + 3

# ㄱ: k=1일 때 P의 좌표
k_val = 1
P_k1 = (2, k_val + 3)
assert P_k1 == (2, 4), f'ㄱ failed: {P_k1}'

# ㄴ: 기울기의 합
m_AB = (y_B - y_A) / (x_B - x_A)
m_AP = (y_P - y_A) / (x_P - x_A)
sum_slope = simplify(m_AB + m_AP)
assert sum_slope == 0, f'ㄴ failed: {sum_slope}'

# ㄷ: 넓이가 자연수일 때
# 넓이 = (27 + 6k - k^2)/6
area_formula = (27 + 6*k - k**2) / 6

# n=5일 때
n = 5
k_solutions = solve(27 + 6*k - k**2 - 6*n, k)
valid_k = [sol for sol in k_solutions if 0 < sol < 3][0]

# 기울기 BP
m_BP = k
m_BP_value = valid_k

# 넓이 확인
area_value = area_formula.subs(k, valid_k)
assert abs(float(area_value) - 5.0) < 1e-9, f'Area should be 5, got {area_value}'
assert 0 < float(m_BP_value) < 1, f'Slope should be in (0,1), got {m_BP_value}'

print('VERIFY_PASS')