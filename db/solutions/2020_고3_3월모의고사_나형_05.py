from sympy import symbols, integrate

t = symbols('t')
f = 2*t

integral1 = integrate(f, (t, 5, 2))
integral2 = integrate(f, (t, 5, 0))
result = integral1 - integral2

print(f'First integral: {integral1}')
print(f'Second integral: {integral2}')
print(f'Result: {result}')
print('VERIFY_PASS' if result == 4 else 'VERIFY_FAIL')