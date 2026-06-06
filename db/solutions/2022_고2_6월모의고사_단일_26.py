import math

a = 36
b = 6

# Condition 1: log_16(a) = 1/log_b(4)
lhs1 = math.log(a) / math.log(16)
rhs1 = 1 / (math.log(4) / math.log(b))

check1 = abs(lhs1 - rhs1) < 1e-10

# Condition 2: log_6(ab) = 3
ab = a * b
lhs2 = math.log(ab) / math.log(6)
check2 = abs(lhs2 - 3) < 1e-10

# Both a, b > 1
check3 = (a > 1) and (b > 1)

if check1 and check2 and check3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')