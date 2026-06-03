import numpy as np

# Verify by numerically computing the limit (large n)
n = 10**7
k = np.arange(1, n+1, dtype=np.float64)
riemann_sum = (2 * np.pi / n) * np.sum(np.sin(np.pi * k / (3 * n)))

# Exact answer
exact = 3.0

print(f'Numerical limit: {riemann_sum:.10f}')
print(f'Expected:        {exact:.10f}')

if abs(riemann_sum - exact) < 1e-4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
