from sympy import Sum, symbols, simplify
n = symbols('n')
result = Sum((-1)**n * n**2, (n, 1, 20)).doit()
print(f'Sum result: {result}')
if result == 210:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')