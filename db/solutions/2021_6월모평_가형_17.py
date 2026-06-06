from itertools import permutations
from fractions import Fraction

def check_conditions(perm):
    pos = {perm[i]: i for i in range(7)}
    pos_4 = pos[4]
    pos_5 = pos[5]
    if pos_4 == 0 or pos_4 == 6 or pos_5 == 0 or pos_5 == 6:
        return False
    if not (perm[pos_4-1] > 4 and perm[pos_4+1] > 4):
        return False
    if not (perm[pos_5-1] < 5 and perm[pos_5+1] < 5):
        return False
    return True

count = sum(1 for perm in permutations([1,2,3,4,5,6,7]) if check_conditions(perm))
total = 5040
result = Fraction(count, total)
if result == Fraction(1, 14):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')