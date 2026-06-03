from sympy import symbols, sqrt, integrate, ln, Rational, simplify
x = symbols('x', positive=True)
# 원래 문제의 함수: y = sqrt((3x+1)/x^2)
y = sqrt((3*x + 1) / x**2)
# 정사각형 단면 넓이 = y^2
S = y**2  # = (3x+1)/x^2
# 부피 = integral from 1 to 2
V = integrate(S, (x, 1, 2))
expected = Rational(1, 2) + 3*ln(2)
if simplify(V - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', 'computed:', V, 'expected:', expected)
