import sympy as sp
a = sp.Symbol('a')
# 연속 조건: (1-a)^2 - 3 = 1
eq = (1-a)**2 - 3 - 1
sols = sp.solve(eq, a)
print(f'Solutions for a: {sols}')
if sols:
    result = sum(sols)
    print(f'Sum of all a values: {result}')
    if result == 2:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')