import math
result = 27**(2/3)
expected = 9
assert abs(result - expected) < 1e-10, f'Expected {expected}, got {result}'
print('VERIFY_PASS')