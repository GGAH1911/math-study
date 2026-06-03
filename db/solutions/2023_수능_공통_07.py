from sympy import sqrt, summation, simplify, symbols, solve
k = symbols('k', integer=True)
a1 = 9/4
d = 9/4
def a(n):
    return n * (9/4)
total = sum(1/(sqrt(a(k)) + sqrt(a(k+1))) for k in range(1, 16))
if abs(total - 2.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: sum = {total}')