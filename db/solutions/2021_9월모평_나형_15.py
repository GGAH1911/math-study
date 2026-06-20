from sympy import symbols, sqrt, Rational

# 주어진 해답: a = 1/3, b = 1/3
a_val = Rational(1, 3)
b_val = Rational(1, 3)

x1, x2 = 2, 8

# 검증: x1 = 2^(ax1+b)
check1 = 2**(a_val * x1 + b_val)
check2 = 2**(a_val * x2 + b_val)

# AB 거리
ab_dist = abs(x2 - x1) * sqrt(2)

# 넓이
area = Rational(1, 2) * (x1 + x2) * (x2 - x1)

if check1 == 2 and check2 == 8 and ab_dist == 6*sqrt(2) and area == 30:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')