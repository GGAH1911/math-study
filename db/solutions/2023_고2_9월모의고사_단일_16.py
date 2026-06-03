import math
c = math.sqrt(6)
a = math.log(c) / math.log(2)
b = math.log(c) / math.log(3)
assert abs(2**a - c) < 1e-10
assert abs(3**b - c) < 1e-10
lhs = a**2 + b**2
rhs = 2 * a * b * (a + b - 1)
assert abs(lhs - rhs) < 1e-10
log6_c = math.log(c) / math.log(6)
assert abs(log6_c - 0.5) < 1e-10
print('VERIFY_PASS')