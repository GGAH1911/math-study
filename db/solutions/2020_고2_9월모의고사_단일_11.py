from sympy import symbols, solve, simplify, Rational

n = symbols('n', positive=True, integer=True)

# 주어진 조건: a_1 = 1/5, r = 2
a1 = Rational(1, 5)
r = 2

# n = 6일 때 검증
n_val = 6

# 등비수열의 합: S_n = a_1 * (r^n - 1) / (r - 1)
S_n = a1 * (r**n_val - 1) / (r - 1)

# 제곱항의 합: S_n^2 = a_1^2 * (r^(2n) - 1) / (r^2 - 1)
S_n_squared = (a1**2) * (r**(2*n_val) - 1) / (r**2 - 1)

# 조건 검증: S_n = (3/13) * S_n^2
left_side = S_n
right_side = Rational(3, 13) * S_n_squared

if simplify(left_side - right_side) == 0:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {left_side} != {right_side}')