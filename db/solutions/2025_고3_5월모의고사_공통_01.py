import math
from math import sqrt, log, exp

# 원래 문제: (3^(1-sqrt(2)))^2 * 9^sqrt(2)
result = (3**(1-sqrt(2)))**2 * (9**sqrt(2))

print(f'Result: {result}')
print(f'Result is close to 9: {abs(result - 9) < 1e-10}')

if abs(result - 9) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')