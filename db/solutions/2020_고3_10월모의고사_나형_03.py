from sympy import Rational, Eq, symbols, solve
PB = symbols('PB', positive=True)
P_A_given_B = Rational(2,3)
P_AB = Rational(2,15)
# P(A|B) = P(A∩B)/P(B)
sol = solve(Eq(P_A_given_B, P_AB/PB), PB)
val = sol[0]
if val == Rational(1,5):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')