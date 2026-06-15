from sympy import symbols, solve, sqrt, simplify

x, y = symbols('x y', real=True)
eq1 = x**2 - 3*x*y + 2*y**2
eq2 = x**2 - y**2 - 9

solutions = solve([eq1, eq2], [x, y])
solutions_sorted = sorted(solutions, key=lambda s: s[0])

alpha1, beta1 = solutions_sorted[0]
alpha2, beta2 = solutions_sorted[1]

result = beta1 - beta2
result_simplified = simplify(result)

if result_simplified == -2*sqrt(3):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result_simplified}')