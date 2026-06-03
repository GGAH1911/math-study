import math
import numpy as np

def riemann_sum(n):
    return sum(1/(2*n + k) for k in range(1, n+1))

n_test = 100000
result_sum = riemann_sum(n_test)
expected = math.log(3/2)

print(f'Riemann sum (n={n_test}): {result_sum:.10f}')
print(f'ln(3/2): {expected:.10f}')
print(f'Difference: {abs(result_sum - expected):.2e}')

if abs(result_sum - expected) < 0.001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')