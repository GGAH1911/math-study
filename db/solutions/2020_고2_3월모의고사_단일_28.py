from itertools import chain, combinations
# U={1..5}, A={1,2},B={2,3,4}. X∩A≠∅ and X∩B≠∅ 인 X 개수?
CANDIDATE = 22
U = [1,2,3,4,5]; A = {1,2}; B = {2,3,4}
subs = chain.from_iterable(combinations(U, r) for r in range(6))
count = sum(1 for X in subs if (set(X) & A) and (set(X) & B))
print('VERIFY_PASS' if count == CANDIDATE else 'VERIFY_FAIL')
