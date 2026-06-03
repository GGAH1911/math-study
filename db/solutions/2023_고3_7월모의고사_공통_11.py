from sympy import symbols, integrate, diff
x = symbols('x')
f = x**3 - 3*x**2 + 2*x
f_prime = diff(f, x)
integral_result = integrate(f_prime, (x, -1, 3))
f_at_4 = f.subs(x, 4)
assert integral_result == 12, f'적분 조건 실패: {integral_result}'
assert f.subs(x, 1+1) + f.subs(x, 1-1) == 0, '점대칭 조건 실패'
assert f_at_4 == 24, f'f(4) 계산 실패: {f_at_4}'
print('VERIFY_PASS')