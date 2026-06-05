from math import gcd

# f(4)
a = 4
factors_4 = {2: 2}  # 4 = 2^2
f_4 = gcd(*[3*e for e in factors_4.values()])

# f(27)
a = 27
factors_27 = {3: 3}  # 27 = 3^3
f_27 = gcd(*[3*e for e in factors_27.values()])

# Verify by checking that a^(3/n) is natural for n = f(a)
import math

# f(4) = 6: check 4^(3/6) = 4^(1/2) = 2
result_4_n6 = 4**(3/6)
if abs(result_4_n6 - round(result_4_n6)) < 1e-9:
    check_4 = 'natural'
else:
    check_4 = 'not natural'

# f(27) = 9: check 27^(3/9) = 27^(1/3) = 3
result_27_n9 = 27**(3/9)
if abs(result_27_n9 - round(result_27_n9)) < 1e-9:
    check_27 = 'natural'
else:
    check_27 = 'not natural'

answer = f_4 + f_27
if answer == 15 and check_4 == 'natural' and check_27 == 'natural':
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')