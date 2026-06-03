import sympy as sp
x, h = sp.symbols('x h')
f = x**3 - 8*x + 7
f_prime = sp.diff(f, x)
f_prime_at_2 = f_prime.subs(x, 2)
print(f'f\'(2) = {f_prime_at_2}')
assert f_prime_at_2 == 4, f'Expected 4, got {f_prime_at_2}'
f_2 = f.subs(x, 2)
f_2_plus_h = f.subs(x, 2 + h)
limit_result = sp.limit((f_2_plus_h - f_2) / h, h, 0)
print(f'Limit result: {limit_result}')
assert limit_result == 4, f'Limit verification failed'
print('VERIFY_PASS')