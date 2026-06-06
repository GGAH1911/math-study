from sympy import symbols, expand, solve
x = symbols('x')
f = -x**2 - 2*x
g = x**2 - 1
h = x**2 - 2*x
sum_func = f + g + h
roots = solve(sum_func, x)
root_sum = sum(roots)
print(f'f(x) + g(x) + h(x) = {expand(sum_func)}')
print(f'Roots: {roots}')
print(f'Sum of roots: {root_sum}')
if root_sum == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')