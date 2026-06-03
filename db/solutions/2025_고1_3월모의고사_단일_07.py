from sympy import symbols, expand
x = symbols('x')
a = x - 1
b = x + 1
c = 2*x + 1
surface_area = 2*(a*b + b*c + c*a)
expanded = expand(surface_area)
print('VERIFY_PASS' if expanded == 10*x**2 + 4*x - 2 else 'VERIFY_FAIL')