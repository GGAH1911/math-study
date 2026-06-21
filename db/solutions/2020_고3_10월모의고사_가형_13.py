from sympy import symbols, sqrt, pi, exp, Rational, N as Neval, Abs

m_val = 10
sigma = 4

# Verify conditions
x8 = abs(8 - m_val)
x14 = abs(14 - m_val)
x2 = abs(2 - m_val)
x16 = abs(16 - m_val)

cond1 = x8 < x14   # f(8) > f(14)
cond2 = x2 > x16   # f(2) < f(16)

# P(X <= 6) = P(Z <= (6-10)/4) = P(Z <= -1)
# = 0.5 - P(0 <= Z <= 1) = 0.5 - 0.3413
result = 0.5 - 0.3413

CANDIDATE = 0.1587

if cond1 and cond2 and abs(result - CANDIDATE) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: cond1={cond1}, cond2={cond2}, computed={result}, candidate={CANDIDATE}')
