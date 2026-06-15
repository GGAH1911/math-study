from itertools import chain, combinations
A = {1,2,3,4}
results = set()
# B = {5,6} union S, S subset of A, with B-A = {5,6} and sum(B)=12
for r in range(len(A)+1):
    for S in combinations(sorted(A), r):
        B = set(S) | {5,6}
        if (B - A) == {5,6} and sum(B) == 12:
            results.add(sum(A - B))
if len(results) == 1 and results.pop() == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')