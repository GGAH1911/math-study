from itertools import combinations
from fractions import Fraction

total = 2**7
count = 0

for i in range(total):
    sequence = [(i >> j) & 1 for j in range(7)]
    heads = sum(sequence)
    
    if heads < 3:
        continue
    
    has_consecutive = any(
        sequence[j] == 1 and sequence[j+1] == 1 
        for j in range(6)
    )
    
    if has_consecutive:
        count += 1

result = Fraction(count, total)
if result == Fraction(11, 16):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')