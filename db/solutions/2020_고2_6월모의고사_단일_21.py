import sympy as sp

x = sp.symbols('x', real=True)
# Confirm x=(2j-1)*pi/8 are exact roots of sin^2(4x)-1=0
for j in range(1, 8):
    val = sp.Rational(2*j-1, 8) * sp.pi
    assert sp.simplify(sp.sin(4*val)**2 - 1) == 0

def f(n):
    # count roots x=(2j-1)*pi/8 with 0 < x < n*pi/12
    # condition: (2j-1)/8 < n/12  <=>  3*(2j-1) < 2*n  (exact integer compare)
    count = 0
    j = 1
    while 3*(2*j-1) < 2*n:
        count += 1
        j += 1
    return count

ns = [n for n in range(1, 600) if f(n) == 33]
total = sum(ns)
CANDIDATE = 297
print('ns =', ns, 'sum =', total)
if ns == [98, 99, 100] and total == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
