from fractions import Fraction

# a_n = 3n+1, b_n = 3n+4
# Partial sum approximation with large N
S = Fraction(0)
for n in range(1, 100001):
    a_n = 3*n + 1
    b_n = 3*n + 4
    S += Fraction(1, a_n * b_n)

expected = Fraction(1, 12)
# Check if partial sum (100000 terms) is very close to 1/12
# Use float comparison
diff = abs(float(S) - float(expected))
if diff < 1e-4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', float(S), float(expected))
