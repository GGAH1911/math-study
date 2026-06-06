from sympy import symbols, solve
a = -1
x_vals = [1, 2, 3, 4, 5]
for x in x_vals:
    lhs = 2*a - x
    rhs = -3*(x - 2)
    satisfies = lhs <= rhs
    print(f'x={x}: {lhs} <= {rhs} is {satisfies}')
count = sum(1 for x in [1,2,3,4,5] if 2*a - x <= -3*(x-2))
print(f'Count of natural numbers: {count}')
if count == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')