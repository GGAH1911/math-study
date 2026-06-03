import math

m = 6
# 원래 방정식: (1/16) * (1/2)^(x-m) = 2^x + 1
# t = 2^x 치환: 2^(m-4) = t(t+1)
# m = 6일 때: t^2 + t - 4 = 0

a, b, c = 1, 1, -4
disc = b**2 - 4*a*c

if disc < 0:
    print('VERIFY_FAIL')
else:
    sqrt_disc = math.sqrt(disc)
    t_positive = (-b + sqrt_disc) / (2*a)
    
    if t_positive > 1:
        x = math.log2(t_positive)
        lhs = (1/16) * (0.5)**(x - m)
        rhs = 2**x + 1
        if abs(lhs - rhs) < 1e-9:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')