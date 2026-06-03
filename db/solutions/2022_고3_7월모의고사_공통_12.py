from sympy import *

n = symbols('n', positive=True, integer=True)

# f(n) = n+1, g(n) = (n+1)/(n-1), p = 110
f = lambda x: x + 1
g = lambda x: Rational(x+1, x-1)
p = 110

# Verify a_n/a_{n-1} = (n+1)/(n-1) gives a_10 = 110
a1 = 2
ratio_product = 1
for k in range(2, 11):
    ratio_product *= Rational(k+1, k-1)
a10 = a1 * ratio_product
assert a10 == 110, f'a10={a10}'

# Verify 3S_n = (n+2)*a_n with a1=2 and the recurrence
a = {1: Rational(2)}
for k in range(2, 11):
    a[k] = a[k-1] * Rational(k+1, k-1)
S = {}
for k in range(1, 11):
    S[k] = sum(a[j] for j in range(1, k+1))

# Check sum condition for several n
for nn in range(1, 11):
    lhs = sum(Rational(3*S[kk], kk+2) for kk in range(1, nn+1))
    rhs = S[nn]
    assert lhs == rhs, f'n={nn}: lhs={lhs}, rhs={rhs}'

# Final answer
fp = f(p)
gp = g(p)
result = Rational(fp, 1) / gp
assert result == 109, f'result={result}'

print('VERIFY_PASS')
