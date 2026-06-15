from sympy import summation, symbols, simplify
k = symbols('k', integer=True)
sum1 = sum((i+1)**2 for i in range(1, 10))
sum2 = sum((i-1)**2 for i in range(1, 11))
result = sum1 - sum2
assert result == 99, f'Expected 99, got {result}'
print('VERIFY_PASS')