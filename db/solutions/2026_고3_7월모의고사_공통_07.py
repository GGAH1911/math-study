from sympy import symbols, integrate, Rational

x, a = symbols('x a')
f = x**3 + x**2 + a

# 조건식
left = integrate(f, (x, 0, 2))
right_base = integrate(f, (x, 0, -2))

# left = Rational(40,3) + right_base를 만족하는 a
# left - Rational(40,3) - right_base = 0
eq = left - Rational(40, 3) - right_base
a_val = (-eq.subs(a, 0)) / eq.coeff(a)

a_val = 2

# 검증
f_check = x**3 + x**2 + a_val
left_check = integrate(f_check, (x, 0, 2))
right_check = Rational(40, 3) + integrate(f_check, (x, 0, -2))

if left_check == right_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')