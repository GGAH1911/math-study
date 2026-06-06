import sympy as sp
x = sp.Symbol('x')
# 방정식: 2^(x-6) = (1/4)^(x^2)
# 2^(x-6) = 2^(-2x^2) => x - 6 = -2x^2
equation = 2*x**2 + x - 6
solutions = sp.solve(equation, x)
print('Solutions:', solutions)
for sol in solutions:
    lhs = 2**(float(sol) - 6)
    rhs = (0.25)**(float(sol)**2)
    if abs(lhs - rhs) < 1e-10:
        pass
    else:
        print('VERIFY_FAIL')
        exit()
result_sum = float(sum(solutions))
if abs(result_sum - (-0.5)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')