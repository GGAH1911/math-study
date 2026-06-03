from fractions import Fraction

a = Fraction(3)
S_partial = Fraction(0)
N = 100000
for n in range(1, N+1):
    term = Fraction(a - 3*n, n) + Fraction(a*n + 6, n + a)
    S_partial += term

# True telescoping limit: 3*(1 + 1/2 + 1/3) = 11/2
S_exact = Fraction(11, 2)
aS = a + S_exact

# Check numerical partial sum is close to 11/2
diff = abs(float(S_partial) - float(S_exact))

# Verify telescoping closed form analytically
# S = 3*(1 + 1/2 + 1/3) because sum_{n=1}^{inf} (3/n - 3/(n+3))
# telescopes to 3*(1/1 + 1/2 + 1/3)
closed = 3 * (Fraction(1) + Fraction(1,2) + Fraction(1,3))
assert closed == Fraction(11, 2), f'closed form wrong: {closed}'
assert aS == Fraction(17, 2), f'a+S wrong: {aS}'
assert diff < 1e-4, f'numerical diff too large: {diff}'

print('VERIFY_PASS')
