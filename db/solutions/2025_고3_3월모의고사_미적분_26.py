import sympy as sp
n = sp.Symbol('n', positive=True, integer=True)
# original condition: sum_{k=1}^{n} (a_k - k^2)/(k+1) = 2n^2 - n
# derived: a_n = 5n^2 + n - 3 for all n>=1
def a(k):
    return 5*k**2 + k - 3

# Verify the original summation for several n values
all_pass = True
for N in range(1, 20):
    lhs = sum((a(k) - k**2) / (k+1) for k in range(1, N+1))
    rhs = 2*N**2 - N
    if abs(lhs - rhs) > 1e-9:
        all_pass = False
        print(f'VERIFY_FAIL at n={N}: lhs={lhs}, rhs={rhs}')
        break

# Verify the limit
import sympy as sp
n = sp.Symbol('n')
expr = (5*n**2 + n - 3) / (n**2 + 1)
limit_val = sp.limit(expr, n, sp.oo)

if all_pass and limit_val == 5:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: summation_ok={all_pass}, limit={limit_val}')
