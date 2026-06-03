from sympy import symbols, solve, simplify
a, b = 7, 2
result = a * b
print(f'a × b = {result}')
assert result == 14, f'Expected 14, got {result}'
verify_point = 2*1 - 7 + 5
assert verify_point == 0, f'Point check failed: {verify_point}'
print('VERIFY_PASS')