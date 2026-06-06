CANDIDATE = 35

from fractions import Fraction

def compute_f(n):
    """
    0 <= x <= 4 범위에서 sin(pi*x) = (-1)^(n+1) / n 의 모든 실근의 합을 계산.
    
    sin(pi*x) = k의 일반해:
    - alpha = arcsin(k) / pi 라 할 때
    - x = alpha + 2m 또는 x = 1 - alpha + 2m
    
    경우의 수:
    1) k = 1: x = 1/2 + 2m => [0,4]에서 x = 1/2, 5/2, 합 = 3
    2) k = -1: x = -1/2 + 2m => [0,4]에서 x = 3/2, 7/2, 합 = 5
    3) 0 < k < 1: 범위 내 해 4개, 합 = 6
    4) -1 < k < 0: 범위 내 해 4개, 합 = 10
    """
    k = Fraction((-1)**(n+1), n)  # 우변: (-1)^(n+1) / n
    k_float = float(k)
    
    if k_float == 1:
        # sin(pi*x) = 1 => pi*x = pi/2 + 2*pi*m => x = 1/2 + 2m
        # [0,4]에서의 해: x = 1/2, 5/2
        roots = [Fraction(1, 2), Fraction(5, 2)]
        return sum(roots)
    
    elif k_float == -1:
        # sin(pi*x) = -1 => pi*x = -pi/2 + 2*pi*m => x = -1/2 + 2m
        # [0,4]에서의 해: x = 3/2, 7/2
        roots = [Fraction(3, 2), Fraction(7, 2)]
        return sum(roots)
    
    elif 0 < k_float < 1:
        # 0 < alpha < 1/2 범위
        # [0,4]에서의 해: alpha, 1-alpha, alpha+2, 3-alpha
        # 합 = alpha + (1-alpha) + (alpha+2) + (3-alpha) = 6
        return Fraction(6)
    
    elif -1 < k_float < 0:
        # -1/2 < alpha < 0 범위
        # [0,4]에서의 해: 1-alpha, alpha+2, 3-alpha, alpha+4
        # 합 = (1-alpha) + (alpha+2) + (3-alpha) + (alpha+4) = 10
        return Fraction(10)
    
    else:
        return Fraction(0)

# 검증: f(1) + f(2) + f(3) + f(4) + f(5) 계산
total_sum = Fraction(0)

for n in range(1, 6):
    f_n = compute_f(n)
    total_sum += f_n

# CANDIDATE와 비교
if total_sum == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")