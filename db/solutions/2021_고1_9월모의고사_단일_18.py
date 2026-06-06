from fractions import Fraction

try:
    # n=5일 때 검증
    n = 5
    
    # 주어진 조건
    target_area = Fraction(1, 42)
    
    # 사각형 POQR의 넓이 계산
    # 넓이 = 1/((n+1)(n+2))
    area_POQR = Fraction(1, (n+1)*(n+2))
    
    # 검증 1: 사각형 넓이가 1/42인지 확인
    assert area_POQR == target_area, f'Area check failed: {area_POQR} != {target_area}'
    
    # f(n) = -1/(n+1), g(n) = 1/(n+2)
    f_k = Fraction(-1, n+1)
    g_k = Fraction(1, n+2)
    
    # 최종 답
    answer = g_k / f_k
    expected = Fraction(-6, 7)
    
    # 검증 2: 답이 -6/7인지 확인
    assert answer == expected, f'Answer check failed: {answer} != {expected}'
    
    # 검증 3: 방정식 (n+1)(n+2) = 42 확인
    assert (n+1)*(n+2) == 42, f'Quadratic check failed'
    
    print('VERIFY_PASS')
except AssertionError as e:
    print(f'VERIFY_FAIL: {str(e)}')
except Exception as e:
    print(f'VERIFY_FAIL: {str(e)}')