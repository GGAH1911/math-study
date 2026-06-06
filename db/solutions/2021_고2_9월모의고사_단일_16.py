from fractions import Fraction
a = {i: sum(Fraction(1, k) for k in range(1, i+1)) for i in range(1, 8)}
p = Fraction(1, 2)
f_m = lambda m: Fraction(m, 2)
g_m = lambda m: Fraction(1, m+2)
result = p + f_m(5) / g_m(3)
assert result == 13, f'Expected 13, got {result}'
print('VERIFY_PASS')