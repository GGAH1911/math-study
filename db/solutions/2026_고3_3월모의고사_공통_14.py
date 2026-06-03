from sympy import *
a = -3*sqrt(2)/2
b = Rational(3,2)
# Check alpha = f(7pi/4) = 0
alpha = a*cos(Rational(7,4)*pi) + b
assert simplify(alpha) == 0, f'alpha={simplify(alpha)}'
# Check beta = f(5pi/4) = 3
beta = a*cos(Rational(5,4)*pi) + b
assert simplify(beta) == 3, f'beta={simplify(beta)}'
# Verify S(t)=7pi/4 for all 4 candidates
# t=0: f=0 -> sols x=0 (piece1) + x=7pi/4 (piece2)
S0 = Integer(0) + Rational(7,4)*pi
assert simplify(S0 - Rational(7,4)*pi) == 0
# t=pi/2: f=3 -> sols x=pi/2 (piece1) + x=5pi/4 (piece2)
S1 = pi/2 + Rational(5,4)*pi
assert simplify(S1 - Rational(7,4)*pi) == 0
# t=5pi/4: f(5pi/4)=3 same as above
S2 = pi/2 + Rational(5,4)*pi
assert simplify(S2 - Rational(7,4)*pi) == 0
# t=7pi/4: f(7pi/4)=0 same as t=0
S3 = Integer(0) + Rational(7,4)*pi
assert simplify(S3 - Rational(7,4)*pi) == 0
# Verify a^2+b^2
result = simplify(a**2 + b**2)
assert result == Rational(27,4), f'got {result}'
print('a^2+b^2 =', result)
print('VERIFY_PASS')