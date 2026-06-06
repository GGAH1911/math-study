from sympy import *
k = symbols('k')

def OA2(kv): return (kv-2)**2 + 4
def OB2(kv): return (kv+2)**2 + 4
AB2 = 16

sol1 = solve(OA2(k) - OB2(k), k)
sol2 = solve(OA2(k) - AB2, k)
sol3 = solve(OB2(k) - AB2, k)

all_k = list(set(sol1 + sol2 + sol3))
n_val = len(all_k)
M_val = max(all_k)

result = n_val + M_val
expected = 7 + 2*sqrt(3)

if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Got: {result}, Expected: {expected}')
