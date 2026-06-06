import sympy as sp
from sympy import symbols, log, solve, Rational

# 역대입 검증
x1, x2 = 2, 8
a = Rational(1, 3)
b = Rational(1, 3)

# 원래 곡선 방정식에 대입
result1 = 2**(a*x1 + b)
result2 = 2**(a*x2 + b)

# x1, x2가 y=2^(ax+b) 위의 점인지 확인
if abs(float(result1) - x1) < 1e-9 and abs(float(result2) - x2) < 1e-9:
    # AB 거리 확인
    AB = ((x2 - x1)**2 + (x2 - x1)**2)**0.5
    if abs(AB - 6*2**0.5) < 1e-9:
        # 넓이 확인
        area = (x1 + x2) * (x2 - x1) / 2
        if abs(area - 30) < 1e-9:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')