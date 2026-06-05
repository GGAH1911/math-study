import sympy as sp
from sympy import sqrt, symbols, solve

# 검증: 주어진 조건으로 a=5, b^2=14가 맞는지 확인
a_sq = 25
b_sq = 14

# 초점까지의 거리
c_sq_ellipse = a_sq - 7
c_sq_hyperbola = 4 + b_sq

# c^2 값이 같은지 확인
if c_sq_ellipse == c_sq_hyperbola:
    c_val = sqrt(c_sq_ellipse)
    
    # P가 타원 위의 점이므로: PF + PF' = 2a
    # PF = 3이면 PF' = 2a - 3
    PF = 3
    expected_PF_prime_ellipse = 2*5 - 3  # = 7
    
    # P가 쌍곡선의 우측 가지 위의 점이므로: PF' - PF = 4
    expected_PF_prime_hyperbola = PF + 4  # = 7
    
    if expected_PF_prime_ellipse == expected_PF_prime_hyperbola:
        result = a_sq + b_sq
        if result == 39:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')