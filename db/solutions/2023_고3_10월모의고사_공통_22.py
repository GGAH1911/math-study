import sympy as sp
x = sp.Symbol('x')

# f(x) = -3/4 * (x-4)^2 * (x - 21/2)
c = -sp.Rational(3, 4)
f = c * (x - 4)**2 * (x - sp.Rational(21, 2))

# Calculate g(10)
g_10 = f.subs(x, 10)
print(f'g(10) = {g_10}')

# Verify it equals 27/2
expected = sp.Rational(27, 2)
if g_10 == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')