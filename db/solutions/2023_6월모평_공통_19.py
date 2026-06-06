from sympy import symbols, diff, solve, Eq

CANDIDATE = '2'

# 문제에서 주어진 함수: f(x) = x^4 + ax^2 + b
x, a, b = symbols('x a b', real=True)
f = x**4 + a*x**2 + b

# 도함수 계산
f_prime = diff(f, x)  # 4x^3 + 2ax
f_double_prime = diff(f_prime, x)  # 12x^2 + 2a

# 조건 1: x=1에서 극소 => f'(1) = 0
# f'(1) = 4 + 2a = 0 => a = -2
a_value = solve(Eq(f_prime.subs(x, 1), 0), a)[0]

# a를 대입한 함수들
f_with_a = f.subs(a, a_value)
f_prime_with_a = f_prime.subs(a, a_value)
f_double_prime_with_a = f_double_prime.subs(a, a_value)

# 극값 위치: f'(x) = 4x^3 - 4x = 4x(x^2-1) = 0 => x = -1, 0, 1
critical_points = solve(f_prime_with_a, x)

# 조건 2: 극댓값이 4
# 극대점은 x=0 (f''(0) = -4 < 0이므로 극대)
# f(0) = b = 4 => b = 4
max_point = 0
b_value = solve(Eq(f_with_a.subs(x, max_point), 4), b)[0]

# === 원래 조건으로부터의 검증 ===
# 조건 1: x=1에서 f'(1) = 0인가?
verify_f_prime_at_1 = f_prime_with_a.subs(x, 1) == 0

# 조건 1: x=1에서 f''(1) > 0인가? (극소 판정)
verify_f_double_prime_at_1 = f_double_prime_with_a.subs(x, 1) > 0

# 조건 2: 극댓값이 4인가?
max_value = f_with_a.subs([(x, 0), (b, b_value)])
verify_max_value = max_value == 4

# CANDIDATE 검증: a + b = 2인가?
calculated_sum = a_value + b_value
verify_candidate = calculated_sum == int(CANDIDATE)

if verify_f_prime_at_1 and verify_f_double_prime_at_1 and verify_max_value and verify_candidate:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')