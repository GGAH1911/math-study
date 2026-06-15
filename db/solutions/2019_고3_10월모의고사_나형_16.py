import sympy as sp
a, alpha, beta = sp.symbols('a alpha beta', real=True)

# 조건 설정
beta_minus_alpha = 10  # β - α = 10

# f(β) - f(α) = -500a (적분 계산)
f_diff = -500 * a

# 거리 조건
distance_sq = beta_minus_alpha**2 + f_diff**2
eq_distance = sp.Eq(distance_sq, 676)  # 26² = 676

# a 구하기
a_sol = sp.solve(eq_distance, a)
print(f'a solutions: {a_sol}')

# 극값의 차
for a_val in a_sol:
    extreme_diff = 500 * sp.Abs(a_val)
    result = sp.simplify(extreme_diff)
    if result == 24:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: got {result}')