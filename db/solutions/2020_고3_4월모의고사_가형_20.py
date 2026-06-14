from itertools import product as iproduct

X = [1, 2, 3, 4, 5]

def check(f_vals):
    # f_vals: tuple of length 5, f_vals[i] = f(i+1)
    f = {i+1: f_vals[i] for i in range(5)}
    A = set(f.values())
    B = set(f[a] for a in A)
    nA = len(A)
    sumA = sum(A)
    nB = len(B)
    return nA >= 3 and sumA % 3 == 0 and nA > nB

p_count = 0
q_count = 0
r_count = 0

for f_vals in iproduct(X, repeat=5):
    f = {i+1: f_vals[i] for i in range(5)}
    A = set(f.values())
    B = set(f[a] for a in A)
    if not check(f_vals):
        continue
    if A == {1,2,3} and B == {1}:
        p_count += 1
    if A == {1,2,3} and B == {1,2}:
        q_count += 1
    if A == {1,2,4,5} and len(B) < 4:
        r_count += 1

p, q, r = p_count, q_count, r_count
print(f'p={p}, q={q}, r={r}, p+q+r={p+q+r}')
if p == 2 and q == 30 and r == 144 and p+q+r == 176:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
