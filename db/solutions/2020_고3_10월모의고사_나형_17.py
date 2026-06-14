from sympy import symbols, limit, diff, Function, Eq, solve

CANDIDATE = 5

# f(1) = -2, f'(1) = CANDIDATE
# g(x) = x + 1
# 검증: 조건 (가)를 직접 확인

# f(x) = f(1) + f'(1)(x-1) + f''(1)(x-1)^2/2 + ... 형태
# 테일러 근처에서: f(x) ≈ -2 + CANDIDATE(x-1) + ...

x = symbols('x')
f_1 = -2  # f(1)
f_prime_1 = CANDIDATE  # f'(1)

# 분자: f(x)(x+1) + 4
# ≈ [-2 + CANDIDATE(x-1)](x+1) + 4
# = -2(x+1) + CANDIDATE(x-1)(x+1) + 4
# = -2x - 2 + CANDIDATE(x-1)(x+1) + 4
# = -2x + 2 + CANDIDATE(x-1)(x+1)
# = -2(x-1) + CANDIDATE(x-1)(x+1)
# = (x-1)[-2 + CANDIDATE(x+1)]

# 극한: lim_{x→1} [f'(x)(x+1) + f(x)]
# x=1에서: f'(1)(1+1) + f(1) = 2*CANDIDATE - 2

limit_value = 2 * f_prime_1 + f_1

if limit_value == 8:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")