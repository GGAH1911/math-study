import numpy as np
from fractions import Fraction

def verify_limit():
    # 원래 식 정의
    def f(n):
        numerator = (1/2)**n + (1/3)**(n+1)
        denominator = (1/2)**(n+1) + (1/3)**n
        return numerator / denominator
    
    # n이 충분히 클 때 값들 계산
    values = [f(n) for n in range(100, 200, 10)]
    
    # 모두 2에 가까운지 확인 (오차 < 1e-10)
    all_close_to_2 = all(abs(v - 2.0) < 1e-8 for v in values)
    
    if all_close_to_2:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
        print(f'Values near n=150: {f(150)}')

verify_limit()