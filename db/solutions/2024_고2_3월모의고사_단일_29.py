import sympy as sp
from sympy import symbols, expand, div, Poly

x = symbols('x')
a, b = -2, 1

# 원래 함수 정의
f = x**4 + (a+2)*x**3 + b*x**2 + a*x + 6

# 우리의 인수분해
g = x**2 + 2*x + 3
h = x**2 - 2*x + 2

# f(x) = g(x) * h(x) 검증
product = expand(g * h)
print('f(x):', f)
print('g(x)*h(x):', product)
assert product == f, 'VERIFY_FAIL'

# 나머지 조건: h(x) = g(x)*q + (-4x-1)
quotient, remainder = div(h, g, domain='ZZ')
print('h(x) ÷ g(x): quotient =', quotient, ', remainder =', remainder)
assert remainder == -4*x - 1, 'VERIFY_FAIL'

# 조건 (가): f(x)는 실근을 갖지 않음
f_roots = sp.solve(f, x)
print('f(x)의 근:', f_roots)
for root in f_roots:
    if root.is_real:
        print('VERIFY_FAIL')
        exit()

# g(x), h(x) 모두 항상 양수 확인
g_discriminant = 4 - 12
h_discriminant = 4 - 8
print('g(x) 판별식:', g_discriminant, '(음수 ✓)')
print('h(x) 판별식:', h_discriminant, '(음수 ✓)')
assert g_discriminant < 0 and h_discriminant < 0, 'VERIFY_FAIL'

print('VERIFY_PASS')