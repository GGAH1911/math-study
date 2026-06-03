import sympy as sp

# 함수 정의
x, t = sp.symbols('x t', real=True)
a_val = -2

# f(x) = 3x^2 - 4x - 5
f = lambda x_val: 3*x_val**2 - 4*x_val - 5

# 원래 주어진 함수방정식 검증
# xf(x) = 2x^3 + ax^2 + 3a + ∫_1^x f(t)dt

x_test = sp.Symbol('x', real=True)
f_expr = 3*x_test**2 - 4*x_test - 5

# 좌변
lhs = x_test * f_expr

# 우변
integral = sp.integrate(f_expr, (x_test, 1, x_test))
rhs = 2*x_test**3 + a_val*x_test**2 + 3*a_val + integral

# 전개 및 정리
lhs_expanded = sp.expand(lhs)
rhs_expanded = sp.expand(rhs)

if sp.simplify(lhs_expanded - rhs_expanded) == 0:
    print('원래 식 확인: PASS')
else:
    print('원래 식 확인: FAIL')

# 조건 f(1) = ∫_0^1 f(t)dt 검증
f_at_1 = f(1)
integral_0_to_1 = sp.integrate(f_expr, (x_test, 0, 1))

if f_at_1 == integral_0_to_1:
    print('조건 f(1) = ∫_0^1 f(t)dt: PASS')
else:
    print('조건 f(1) = ∫_0^1 f(t)dt: FAIL')

# 최종 답 계산
f_3 = f(3)
answer = a_val + f_3

if answer == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')