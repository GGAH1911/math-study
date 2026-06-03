import math
from math import pi, tan, sqrt

x = 7*pi/6
result = sqrt(3) * tan(x)
print('VERIFY_PASS' if abs(result - 1.0) < 1e-10 else 'VERIFY_FAIL')