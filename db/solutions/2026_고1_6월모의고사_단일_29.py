from sympy import symbols, expand, factor
x = symbols('x')
B = x**2 + 2*x
A = B*(B + x) + (B - x**2)
A_expanded = expand(A)
print('A(x) =', A_expanded)
result = A_expanded.subs(x, 2)
print('A(2) =', result)
if result == 84:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')