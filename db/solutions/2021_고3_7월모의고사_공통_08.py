from sympy import symbols, solve, simplify

# 변수 정의
a, r = symbols('a r', real=True, positive=True)

# 등비수열의 합
S2 = a * (1 + r)
S3 = a * (1 + r + r**2)

# 조건들
cond1 = 2*a - (S2 + S3)  # = 0
cond2 = r**2 - 64*a**2   # = 0

# 방정식 풀기
sol = solve([cond1, cond2], [a, r])
print('Solutions:', sol)

# a=1/4, r=-2 검증 (r=-2는 음수이므로 별도 처리)
a_val = 1/4
r_val = -2

# 조건 1 검증: 2a = S2 + S3
S2_val = a_val * (1 + r_val)
S3_val = a_val * (1 + r_val + r_val**2)
cond1_check = (2 * a_val) - (S2_val + S3_val)
print(f'Condition 1 check: 2a={2*a_val}, S2+S3={S2_val + S3_val}, diff={cond1_check}')

# 조건 2 검증: r^2 = 64a^2
cond2_check = r_val**2 - 64*a_val**2
print(f'Condition 2 check: r^2={r_val**2}, 64a^2={64*a_val**2}, diff={cond2_check}')

# a5 계산
a5 = a_val * (r_val ** 4)
print(f'a5 = {a_val} * {r_val}^4 = {a5}')

if abs(cond1_check) < 1e-10 and abs(cond2_check) < 1e-10 and a5 == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')