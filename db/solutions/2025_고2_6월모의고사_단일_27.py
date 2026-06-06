from sympy import *

# 모든 가능한 (k, m, n) 쌍 검증
valid_pairs = []
for k in [1, 2, 3, 4, 6, 12]:
    n = k**2
    m = 4*k
    
    # 조건 (가): sqrt(m) = 2 * n^(1/4)
    sqrt_m = sqrt(m)
    two_fourth_root_n = 2 * n**(Rational(1,4))
    cond_a = simplify(sqrt_m - two_fourth_root_n) == 0
    
    # 조건 (나): 3m/n 이 자연수
    ratio = 3*m / n
    cond_b = ratio == int(ratio) and ratio > 0
    
    if cond_a and cond_b:
        valid_pairs.append((k, m, n))

m_values = [m for k, m, n in valid_pairs]
total = sum(m_values)

if total == 112 and len(valid_pairs) == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')