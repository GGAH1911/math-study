from sympy import *
x = symbols('x')
inequality = 2**(x-4) - (Rational(1,2))**(x-2)
for val in [1, 2, 3, 4, 5]:
    result = inequality.subs(x, val)
    is_satisfied = float(result) <= 0
    print(f'x={val}: {float(2**(val-4))} <= {float((Rational(1,2))**(val-2))} ? {is_satisfied}')
natural_nums = [v for v in [1,2,3,4,5] if float(2**(v-4)) <= float((Rational(1,2))**(v-2))]
total = sum(natural_nums)
print(f'Natural numbers satisfying: {natural_nums}')
print(f'Sum: {total}')
if total == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')