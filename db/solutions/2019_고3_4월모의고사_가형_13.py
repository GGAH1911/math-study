from sympy import *
x, a = symbols('x a', real=True)
t = symbols('t', real=True)

# f(x) = 3^x * ln(3) 일 때
f = lambda x_val: 3**x_val * ln(3)
f_prime = lambda x_val: 3**x_val * (ln(3))**2

# a = -1 로 검증
a_val = -1

# 좌변: x*f(x)
lhs = x * f(x)

# 우변: 3^x + a + ∫[0,x] t*f'(t) dt
# ∫[0,x] t*3^t*(ln 3)^2 dt 계산
integrand = t * 3**t * (ln(3))**2
antiderivative = integrate(integrand, t)
integral_val = antiderivative.subs(t, x) - antiderivative.subs(t, 0)
rhs = 3**x + a_val + integral_val

# 좌변과 우변이 같은지 확인
difference = simplify(lhs - rhs)
if difference == 0:
    result = f(-1)
    print(f'f(a) = f(-1) = {result}')
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')