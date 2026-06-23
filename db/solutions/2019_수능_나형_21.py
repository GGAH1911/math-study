from sympy import symbols, solve, simplify, Rational
a = symbols('a', integer=True)
x = symbols('x', real=True)

# a = 3 검증
a_val = 3
f_poly = x**3 + a_val*x**2 + 3*x
g_expr = (x + 3) / (x**2 + a_val*x + 3)

# 조건 검증
# 1. f(x)*g(x) = x(x+3)
product = simplify(f_poly * g_expr)
expected = x * (x + 3)
check1 = simplify(product - expected) == 0

# 2. g(0) = 1
g_at_0 = 1 / 3
check2 = g_at_0 == 1

# f(0) = 0 검증
f_at_0 = f_poly.subs(x, 0)
check3 = f_at_0 == 0

# f(1) = 자연수
f_at_1 = f_poly.subs(x, 1)
check4 = f_at_1 == 7

# g(2) 계산
g_at_2 = g_expr.subs(x, 2)
expected_g2 = Rational(5, 13)
check5 = g_at_2 == expected_g2

# 판별식 확인
discriminant = a_val**2 - 12
check6 = discriminant < 0

if check1 and check3 and check4 and check5 and check6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: check1={check1}, check3={check3}, check4={check4}, check5={check5}, check6={check6}')