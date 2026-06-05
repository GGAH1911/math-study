from sympy import symbols, solve, simplify

# 주어진 조건: S_n = n^2 - 5n
# 등차수열이므로 S_n = n(a_1 + a_n)/2 = n(2*a_1 + (n-1)*d)/2

a1, d = symbols('a1 d')
n = symbols('n', positive=True, integer=True)

# 등차수열 합 공식
S_n = n * (2*a1 + (n-1)*d) / 2

# 주어진 합
S_given = n**2 - 5*n

# S_n = S_given을 만족해야 함
eq = S_n - S_given

# n에 대해 정리: 2*a1 + (n-1)*d = 2*n - 10
eq_simplified = 2*a1 + (n-1)*d - (2*n - 10)
eq_simplified = simplify(eq_simplified)

# n의 계수: d = 2
# 상수항: 2*a1 - d = -10
sol = solve([d - 2, 2*a1 - d + 10], [a1, d])

a1_val = sol[a1]
d_val = sol[d]

# 답: a_1 + d
answer = a1_val + d_val

# 검증: 원래 조건에 역대입
S_check = n * (2*a1_val + (n-1)*d_val) / 2
S_expected = n**2 - 5*n

verify = simplify(S_check - S_expected)

if verify == 0 and answer == -2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')