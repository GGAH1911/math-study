from sympy import symbols, Eq, solve, sqrt
import math

CANDIDATE = 44

# 두 조건식: 10a + b = 44, a^2 - b = 12
# 이를 동시에 풀어 a, b 구하기
# b = 44 - 10a를 두 번째 식에 대입:
# a^2 - (44 - 10a) = 12
# a^2 + 10a - 56 = 0

# 근의 공식으로 풀기
discriminant = 10**2 + 4*1*56
a_candidate_1 = (-10 + math.sqrt(discriminant)) / 2
a_candidate_2 = (-10 - math.sqrt(discriminant)) / 2

# 자연수 a 찾기
a_val = None
if discriminant == 324 and a_candidate_1 == 4.0:  # discriminant = 18^2
    a_val = 4

if a_val is not None and a_val > 0:
    # b 계산
    b_val = 44 - 10*a_val
    
    # 모든 조건 검증
    condition_1 = (a_val > 0 and b_val > 0)  # 자연수 조건
    condition_2 = (a_val**2 - b_val == 12)    # 핵심 도출 조건
    condition_3 = (b_val < a_val**2 / 2)      # 불연속 조건
    c = b_val - a_val**2
    condition_4 = (c < 0)                     # c < 0 필수
    condition_5 = (abs(c) == a_val**2 - b_val)  # |c| 정의
    condition_6 = (10*a_val + b_val == CANDIDATE)  # 최종 검증
    
    # 추가 검증: T = 2(a^2 - b) = 24
    T = 2 * (a_val**2 - b_val)
    condition_7 = (T == 24)
    
    # 모든 조건 확인
    all_pass = all([condition_1, condition_2, condition_3, condition_4, 
                    condition_5, condition_6, condition_7])
    
    if all_pass:
        print("VERIFY_PASS")
    else:
        print("VERIFY_FAIL")
else:
    print("VERIFY_FAIL")