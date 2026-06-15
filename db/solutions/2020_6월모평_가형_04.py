from sympy import Rational, symbols, Eq, solve
# Unknowns: probabilities of disjoint regions
# a = P(A only) = P(A cap B^C), c = P(A cap B), b = P(A^C cap B)
a, b, c = symbols('a b c', nonnegative=True)
P_AuB = Rational(3,4)      # given P(A union B)
P_AcB = Rational(2,3)      # given P(A^C cap B)
# A union B = (A only) + (A and B) + (B only); B only = A^C cap B
eqs = [Eq(a + c + b, P_AuB), Eq(b, P_AcB)]
sol = solve(eqs, [a, c, b], dict=True)[0]
# P(A) = a + c
b_val = sol[b]
# a + c = P(A union B) - (A^C cap B)
P_A = P_AuB - b_val
print('VERIFY_PASS' if P_A == Rational(1,12) else 'VERIFY_FAIL')
