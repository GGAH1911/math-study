import math
from sympy import symbols, solve

CANDIDATE = 360

# 주어진 조건들로부터 유도된 p에 대한 4차 방정식:
# k^2 = 4p(p+a) = CANDIDATE에서 p(p+a) = 90
# 넓이 조건: (a+p)*2*sqrt(pa) = 4p + 24
# (90/p)*sqrt(p*(90/p - p)) = 2p + 12
# 정리하면: 4p^4 + 48p^3 + 8244p^2 - 729000 = 0

p = symbols('p', real=True)
eq_quartic = 4*p**4 + 48*p**3 + 8244*p**2 - 729000

# 방정식 풀기
p_solutions = solve(eq_quartic, p)

# 양의 실근 찾기 및 검증
verification_passed = False

for p_val in p_solutions:
    try:
        p_float = float(p_val)
    except (TypeError, ValueError):
        continue
    
    if p_float <= 0:
        continue
    
    # a 계산: p(p+a) = 90에서
    a_val = 90.0 / p_float - p_float
    
    if a_val <= 0:
        continue
    
    # 포물선: b^2 = 4pa
    b_squared = 4 * p_float * a_val
    b_val = math.sqrt(b_squared)
    
    # 점들 정의
    H = (-p_float, b_val)
    F = (p_float, 0)
    A = (a_val, b_val)
    
    # 조건 1 검증: k^2 = 4p(p+a) = CANDIDATE
    k_squared_from_condition = 4 * p_float * (p_float + a_val)
    
    # 조건 2 검증: 넓이 = 1/2 * (a+p) * b = 2p + 12
    # (A와 H가 같은 높이 y=b이므로, 밑변=a+p, 높이=b)
    area_calc = 0.5 * (a_val + p_float) * b_val
    area_expected = 2 * p_float + 12
    
    # 조건 3 검증: k = |HF|
    k_direct = math.sqrt((F[0] - H[0])**2 + (F[1] - H[1])**2)
    k_squared_direct = k_direct ** 2
    
    # 모든 조건 만족 확인
    cond1_ok = abs(k_squared_from_condition - CANDIDATE) < 1e-8
    cond2_ok = abs(area_calc - area_expected) < 1e-8
    cond3_ok = abs(k_squared_direct - CANDIDATE) < 1e-8
    
    if cond1_ok and cond2_ok and cond3_ok:
        verification_passed = True
        break

if verification_passed:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")