from sympy import symbols, solve, simplify
x, a = symbols('x a')
quadratic = x**2 + a*x + 6
# 부등식의 해가 2 < x < 3이려면, 방정식의 근이 2와 3이어야 함
roots = solve(quadratic.subs(a, -5), x)
print(f'근: {roots}')
verify = (roots == [2, 3] or roots == [3, 2])
if verify:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')