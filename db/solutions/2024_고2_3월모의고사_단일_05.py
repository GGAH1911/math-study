from sympy import symbols, expand
a = -14
f_2 = 2**3 + a * 2**2 + 12
remainder_given = 2*a - 8
assert f_2 == remainder_given, f'f(2)={f_2}, expected remainder={remainder_given}'
print('VERIFY_PASS')