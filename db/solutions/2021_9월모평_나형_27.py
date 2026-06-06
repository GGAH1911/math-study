from fractions import Fraction
a, b, c, d = Fraction(1,3), Fraction(1,2), 0, Fraction(1,6)
E_X = 1*a + 2*b + 3*c + 4*d
E_X2 = 1*a + 4*b + 9*c + 16*d
assert E_X == 2 and E_X2 == 5, 'X conditions failed'
E_Y = 11*a + 21*b + 31*c + 41*d
E_Y2 = 121*a + 441*b + 961*c + 1681*d
V_Y = E_Y2 - E_Y**2
ans = E_Y + V_Y
assert ans == 121, f'Expected 121, got {ans}'
print('VERIFY_PASS')