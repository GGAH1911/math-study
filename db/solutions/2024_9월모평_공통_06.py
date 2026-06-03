from sympy import symbols, diff, simplify

x = symbols('x')
f = x**3 - 3*x**2 - 9*x + 1

# 극댓값은 x = -1에서
result = f.subs(x, -1)
print('VERIFY_PASS' if result == 6 else 'VERIFY_FAIL')