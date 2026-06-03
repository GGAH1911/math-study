import sympy as sp
import numpy as np

# 변수 정의
x, k = sp.symbols('x k', real=True)

# k = 4로 설정
k_val = 4

# 이차함수와 직선의 교점 구하기
eq = sp.Eq(sp.Rational(1,2) * (x - k_val)**2, x)
roots = sp.solve(eq, x)
roots.sort()

if len(roots) == 2:
    x_A, x_B = roots[0], roots[1]
    
    # 점 A, B의 좌표 (직선 위이므로 y = x)
    A = (x_A, x_A)
    B = (x_B, x_B)
    
    # 점 C, D는 x축에 내린 수선의 발
    C = (x_A, 0)
    D = (x_B, 0)
    
    # 선분 CD의 길이
    CD_length = abs(x_B - x_A)
    
    # 검증: 점들이 원래 곡선 위에 있는지
    point_A_on_curve = sp.Rational(1,2) * (x_A - k_val)**2 == x_A
    point_B_on_curve = sp.Rational(1,2) * (x_B - k_val)**2 == x_B
    
    # CD의 길이가 6인지 확인
    if CD_length == 6 and point_A_on_curve and point_B_on_curve:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')