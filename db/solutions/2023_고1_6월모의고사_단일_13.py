from sympy import symbols, expand, div
x = symbols('x')
a = 1
P = x**5 + a*x**2 + (a+1)*x + 2
Q, R = div(P, x - 1)
Q_at_2 = Q.subs(x, 2)
answer = a + Q_at_2
result = 'VERIFY_PASS' if answer == 37 else 'VERIFY_FAIL'
print(result)