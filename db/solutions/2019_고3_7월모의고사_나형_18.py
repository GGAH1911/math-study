from itertools import permutations
from fractions import Fraction

x_counts = {0: 0, 1: 0, 2: 0, 3: 0}

for perm in permutations(range(1, 6), 3):
    a1, a2, a3 = perm
    x = (a1 != 1) + (a2 != 2) + (a3 != 3)
    x_counts[x] += 1

prob_1 = Fraction(x_counts[1], 60)
prob_2 = Fraction(x_counts[2], 60)
prob_3 = Fraction(x_counts[3], 60)

e_x = Fraction(0*x_counts[0] + 1*x_counts[1] + 2*x_counts[2] + 3*x_counts[3], 60)

a = prob_1
b = prob_2
c = e_x

result = 10*a + 20*b + 5*c

if result == 20:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')