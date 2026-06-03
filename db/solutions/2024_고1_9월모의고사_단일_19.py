from sympy import symbols, expand

x = symbols('x')
# f(x) = -2x^2 - 3x + 14, g(x) = 2x^2 + x - 10
f = lambda t: -2*t**2 - 3*t + 14
g = lambda t: 2*t**2 + t - 10

# 조건 (가) 검증: f(x) - g(x) = -4(x+3)(x-2)
diff_expected = expand(-4*(x+3)*(x-2))
f_expr = -2*x**2 - 3*x + 14
g_expr = 2*x**2 + x - 10
f_minus_g = expand(f_expr - g_expr)
assert f_minus_g == diff_expected, f'(가) 실패: {f_minus_g} != {diff_expected}'

# 조건 (나) 검증: f(-3) + g(2) = 5
assert f(-3) + g(2) == 5, f'(나) 실패: {f(-3) + g(2)} != 5'

# 직선 AB 기울기 = -1
slope = (f(2) - f(-3)) / (2 - (-3))
assert slope == -1, f'기울기 실패: {slope} != -1'

# 최종 답 검증
answer = f(-1) + g(-1)
assert answer == 6, f'답 실패: {answer} != 6'

print('VERIFY_PASS')