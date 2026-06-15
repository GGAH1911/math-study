from itertools import combinations_with_replacement
# f:X→X (X={1..6}) 비감소, f(3)·f(6)이 3의 배수. 개수?
CANDIDATE = 327
count = sum(1 for s in combinations_with_replacement(range(1,7), 6) if (s[2]*s[5]) % 3 == 0)
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
