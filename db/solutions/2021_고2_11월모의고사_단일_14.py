from sympy import symbols, solve, simplify, Rational

r = symbols('r', real=True, positive=True)

# 공비 구하기
# 조건: (S_6)/(S_5 - S_2) = a_2 / 2
# S_n = 3 * (r^n - 1) / (r - 1)
a1 = 3
a2 = 3 * r
S2 = 3 * (r**2 - 1) / (r - 1)
S5 = 3 * (r**5 - 1) / (r - 1)
S6 = 3 * (r**6 - 1) / (r - 1)

eq = S6 / (S5 - S2) - a2 / 2
eq_simplified = simplify(eq)

sol_r = solve(eq_simplified, r)
print(f"r의 해: {sol_r}")

# r = 2^(1/3)인 경우 확인
r_val = 2**(Rational(1, 3))
a4 = 3 * r_val**3
print(f"r = 2^(1/3), a_4 = {a4}")

# 조건식 검증
S2_val = 3 * (r_val**2 - 1) / (r_val - 1)
S5_val = 3 * (r_val**5 - 1) / (r_val - 1)
S6_val = 3 * (r_val**6 - 1) / (r_val - 1)
lhs = S6_val / (S5_val - S2_val)
rhs = a2.subs(r, r_val) / 2

if abs(simplify(lhs - rhs)) < 1e-10 or simplify(lhs - rhs) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: lhs={lhs}, rhs={rhs}')