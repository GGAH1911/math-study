from itertools import product
U = {1, 2, 4, 8, 16, 32}
solutions = []
for mask_A in product([0,1], repeat=6):
    for mask_B in product([0,1], repeat=6):
        elements = sorted(U)
        A = {elements[i] for i in range(6) if mask_A[i]}
        B = {elements[i] for i in range(6) if mask_B[i]}
        if A & B == {2, 8} and ((U - A) | B) == {1, 2, 8, 16}:
            solutions.append(A)
assert len(solutions) >= 1, 'no solution'
sums = {sum(A) for A in solutions}
print('VERIFY_PASS' if sums == {46} else 'VERIFY_FAIL')
