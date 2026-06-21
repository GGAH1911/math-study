from sympy import Rational, simplify
P_A = Rational(1,2)
P_B = Rational(1,2)
P_white_given_A = Rational(21,50)
P_white_given_B = Rational(14,50)
P_A_and_white = P_A * P_white_given_A
P_B_and_white = P_B * P_white_given_B
P_white = P_A_and_white + P_B_and_white
P_A_given_white = simplify(P_A_and_white / P_white)
CANDIDATE = Rational(3,5)
print('VERIFY_PASS' if P_A_given_white == CANDIDATE else 'VERIFY_FAIL')