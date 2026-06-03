import math
result = 2 ** (1.5 - math.sqrt(2))
print(f'Computed value: {result}')
if 0.95 < result < 1.15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')