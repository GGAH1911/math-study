from sympy import symbols, limit, simplify, oo, Rational

CANDIDATE = '25'

x = symbols('x')

# 검증된 풀이의 함수들
f = -5*x + 6
g = -2*x**2 + 2*x

# 1. 원래 관계식 확인: xf(x) = (-x/2 + 3)g(x) - x^3 + 2x^2
lhs = x * f
rhs = (-Rational(1, 2)*x + 3) * g - x**3 + 2*x**2

relation_check = (simplify(lhs - rhs) == 0)

# 2. 극한 계산
# lim_{x→2} g(x-1)/(f(x) - g(x))
limit1 = limit(g.subs(x, x-1) / (f - g), x, 2)

# lim_{x→∞} {f(x)}^2 / g(x)
limit2 = limit(f**2 / g, x, oo)

# 3. k 계산
k_value = limit1 * limit2
k_int = int(k_value)

# 4. 검증
if relation_check and k_int == int(CANDIDATE):
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")