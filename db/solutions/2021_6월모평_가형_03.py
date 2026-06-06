from sympy import symbols, solve, simplify

r = symbols('r', positive=True, real=True)
a1 = 1

# 등비수열: a_n = a1 * r^(n-1)
a2 = a1 * r
a3 = a1 * r**2

# 조건: a3 = a2 + 6
eq = a3 - (a2 + 6)
sol = solve(eq, r)
print(f'r 값: {sol}')

# 양수인 공비
r_value = [s for s in sol if s > 0][0]
print(f'공비 r = {r_value}')

# a4 계산
a4 = a1 * r_value**3
print(f'a4 = {a4}')

# 검증: a3 = a2 + 6인지 확인
a2_val = a1 * r_value
a3_val = a1 * r_value**2
verify = simplify(a3_val - (a2_val + 6))
print(f'검증 (a3 - (a2+6) = 0 이어야 함): {verify}')

if a4 == 27 and verify == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')