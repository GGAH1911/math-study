from sympy import symbols, expand, simplify, factor
n = symbols('n')
numerator = n**3 + 1
denominator = n**2 - n + 1
result = simplify(numerator / denominator)
print(f'Simplified: {result}')
assert result == n + 1, 'Factorization check failed'
final_value = result.subs(n, 2026)
assert final_value == 2027, f'Expected 2027, got {final_value}'
print('VERIFY_PASS')