from sympy import symbols, solve
x = symbols('x')
ineq_expr = -2*x - (21 - 4*x)
for test_x in range(1, 15):
    left = (1/9)**test_x
    right = 3**(21 - 4*test_x)
    satisfies = left < right
    print(f'x={test_x}: {satisfies}')
max_nat = max([i for i in range(1, 20) if (1/9)**i < 3**(21-4*i)])
count = max_nat
print(f'Count of natural numbers: {count}')
if count == 10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')