from sympy import symbols, solve, diff, simplify
x = symbols('x', real=True)
# 원래 함수 f(x^3 + x)의 역함수 조건 검증
# g(f(x^3+x)) = x에서 양변 미분하면
# g'(f(x^3+x)) * f'(x^3+x) * (3x^2+1) = 1
# x=1에서: g'(f(2)) * f'(2) * 4 = 1
# f(2)=1이므로: g'(1) * f'(2) * 4 = 1
# 따라서: g'(1) = 1/(4*f'(2))

# f'(2) = 8*g'(1) - 1에 대입
# f'(2) = 8/(4*f'(2)) - 1
# f'(2) = 2/f'(2) - 1
# [f'(2)]^2 = 2 - f'(2)
# [f'(2)]^2 + f'(2) - 2 = 0

fp2 = symbols('fp2', positive=True, real=True)
eq = fp2**2 + fp2 - 2
sol_fp2 = solve(eq, fp2)
print(f'f\'(2) = {sol_fp2}')

f_prime_2 = 1  # 양수 조건에서
g_prime_1 = 1 / (4 * f_prime_2)
g_1 = 1  # 역함수 정의: g(f(1^3+1)) = 1 -> g(f(2)) = 1 -> g(1) = 1

result = g_1 + g_prime_1
expected = 5/4

if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}, expected {expected}')