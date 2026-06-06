import math

# 답: 5a + b = 144
# a = 96/5 = 19.2, b = 48

a = 96/5
b = 48

# 조건 1: 5a = 2b
if abs(5*a - 2*b) < 1e-9:
    cond1 = True
else:
    cond1 = False

# 조건 2: AB = 10
# A의 x좌표: x = 2
# B의 x좌표: x = 3 * 2^(5a/b)
x_A = 2
x_B = 3 * (2 ** (5*a/b))
AB = x_B - x_A

if abs(AB - 10) < 1e-9:
    cond2 = True
else:
    cond2 = False

# 조건 3: f(b) = 2b
# b = 48 >= 3이므로 f(b) = b*log_2(b/3) - 5a
f_b = b * math.log2(b/3) - 5*a

if abs(f_b - 2*b) < 1e-9:
    cond3 = True
else:
    cond3 = False

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')