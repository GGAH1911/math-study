from math import comb
from fractions import Fraction

# Calculate P(A ∩ B): (exactly 1 white in first 3) AND (at least 1 white in last 2)
prob_1_white_in_3 = comb(3, 1) * Fraction(1, 3) * (Fraction(2, 3)**2)
prob_at_least_1_in_2 = 1 - (Fraction(2, 3)**2)
prob_A_and_B = prob_1_white_in_3 * prob_at_least_1_in_2

# Calculate P(B): at least 2 white in 5 trials
prob_0_white = comb(5, 0) * (Fraction(2, 3)**5)
prob_1_white = comb(5, 1) * Fraction(1, 3) * (Fraction(2, 3)**4)
prob_B = 1 - (prob_0_white + prob_1_white)

# Conditional probability P(A|B)
prob_A_given_B = prob_A_and_B / prob_B

# Extract p and q
q = prob_A_given_B.numerator
p = prob_A_given_B.denominator

# Verify gcd(p,q) = 1
from math import gcd
assert gcd(p, q) == 1, f"Not coprime: gcd({p}, {q}) = {gcd(p, q)}"

# Answer
answer = p + q

if answer == 191:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")