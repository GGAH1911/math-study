from sympy import symbols, expand
x = symbols('x')
left = x*(x-4)*(x**2-4*x+7)+12
right = (x-1)*(x+(-3))*(x+(-2))**2
expanded_left = expand(left)
expanded_right = expand(right)
if expanded_left == expanded_right:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')