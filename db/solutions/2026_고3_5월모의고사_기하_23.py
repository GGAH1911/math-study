import math
a_squared = 10
b_squared = 7
c_squared = a_squared - b_squared
c = math.sqrt(c_squared)
print('VERIFY_PASS' if abs(c - math.sqrt(3)) < 1e-10 else 'VERIFY_FAIL')