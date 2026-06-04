import sympy as sp
from sympy import symbols, integrate, Rational

x = symbols('x')
alpha = symbols('alpha', real=True, positive=True)

# Define f(x)
f = Rational(1,2) * x**2 * (x + 1)

# Verify that alpha satisfies the intersection equation
# f(alpha) = -1/2 * alpha + 1
# This gives: alpha^3 + alpha^2 + alpha - 2 = 0
# So: alpha^3 + alpha^2 + alpha = 2

# Key relations
# alpha^3 = 2 - alpha^2 - alpha
# alpha^4 = alpha * alpha^3 = alpha(2 - alpha^2 - alpha) = 2*alpha - alpha^3 - alpha^2
#        = 2*alpha - (2 - alpha^2 - alpha) - alpha^2 = 3*alpha - 2

# A - B calculation
# A = 59/21 - (1/2)*alpha - (1/8)*alpha^4 - (1/12)*alpha^3
# B = (1/8)*alpha^4 + (1/6)*alpha^3 + (1/4)*alpha^2 - alpha + 1

A_expr = Rational(59,21) - Rational(1,2)*alpha - Rational(1,8)*(3*alpha - 2) - Rational(1,12)*(2 - alpha**2 - alpha)
B_expr = Rational(1,8)*(3*alpha - 2) + Rational(1,6)*(2 - alpha**2 - alpha) + Rational(1,4)*alpha**2 - alpha + 1

A_simplified = sp.expand(A_expr)
B_simplified = sp.expand(B_expr)

result = sp.simplify(A_simplified - B_simplified)

if result == Rational(38, 21):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Expected: 38/21, Got: {result}')