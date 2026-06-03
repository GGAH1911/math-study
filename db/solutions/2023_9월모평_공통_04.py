import sympy as sp
a = sp.Symbol('a')
# 연속 조건: x=a에서 좌극한 = 우극한
# 좌극한: -2a+a = -a
# 우극한: a*a-6 = a^2-6
eq = sp.Eq(-a, a**2 - 6)
solutions = sp.solve(eq, a)
print(f'Solutions: {solutions}')
total = sum(solutions)
print(f'Sum of all a: {total}')
if total == -1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')