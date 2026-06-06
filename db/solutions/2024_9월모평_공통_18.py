import sympy as sp

x, a = sp.symbols('x a')
f = (x**2 + 1) * (x**2 + a*x + 3)
f_prime = sp.diff(f, x)

# f'(1) = 32일 때 a를 구함
equation = sp.Eq(f_prime.subs(x, 1), 32)
a_value = sp.solve(equation, a)[0]

# 검증: a = 5일 때 f'(1) = 32인지 확인
f_with_a = (x**2 + 1) * (x**2 + a_value*x + 3)
f_prime_with_a = sp.diff(f_with_a, x)
f_prime_at_1 = f_prime_with_a.subs(x, 1)

if f_prime_at_1 == 32:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')