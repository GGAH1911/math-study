from sympy import Rational, sqrt, simplify

total = Rational(0)
for n in range(1, 6):
    # Tangency condition: m^2 * (n+1)^2 = m^2 + 1  =>  m^2 = 1/(n(n+2))
    m_sq = Rational(1, n * (n + 2))
    m = sqrt(m_sq)
    # Verify tangent point is in Q1
    x_t = n - m_sq * (n + 1) / (m_sq + 1)
    y_t = m * (n + 1) / (m_sq + 1)
    assert x_t > 0, f'x_t not positive for n={n}: {x_t}'
    assert y_t > 0, f'y_t not positive for n={n}: {y_t}'
    total += m_sq

if total == Rational(25, 42):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {total}')
