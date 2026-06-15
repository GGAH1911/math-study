from fractions import Fraction
from itertools import product
# A,B 각 4공. 매 시행 P(A+1)=1/4,P(A-1)=1/4,P(0)=1/2. 4번째 시행 후 처음으로 6. p+q? (q/p)
CANDIDATE = 135
P = {1: Fraction(1,4), -1: Fraction(1,4), 0: Fraction(1,2)}
prob = Fraction(0)
for steps in product([1, 0, -1], repeat=4):
    A = 4; trace = []
    for s in steps:
        A += s; trace.append(A)
    if trace[3] != 6 or 6 in trace[:3]:      # A_4=6 처음
        continue
    pr = Fraction(1)
    for s in steps:
        pr *= P[s]
    prob += pr
print('VERIFY_PASS' if prob.denominator + prob.numerator == CANDIDATE else 'VERIFY_FAIL')
