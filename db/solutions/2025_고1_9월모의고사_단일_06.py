from sympy import symbols, expand, solve
x, a, b = symbols('x a b')
# 원래 이차식
quadratic = x**2 + a*x + b
# a = -8, b = 15을 대입
quadratic_vals = quadratic.subs([(a, -8), (b, 15)])
print(f'이차식: {quadratic_vals}')
roots = solve(quadratic_vals, x)
print(f'근: {roots}')
if roots == [3, 5]:
    result = 15 - (-8)
    print(f'b - a = {result}')
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')