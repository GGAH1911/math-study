from sympy import symbols

CANDIDATE = '6'

# ===== 원래 문제 =====
# 함수: f(x) = x^3 + a*x^2 - (a^2 - 8a)*x + 3
# 조건: 실수 전체의 집합에서 증가
# 구하기: a의 최댓값

# f'(x) = 3x^2 + 2ax - (a^2 - 8a)
# 증가 조건: f'(x) >= 0 for all x in R
# ⟹ (x에 대한 2차식이므로) 판별식 D <= 0

# 판별식: D = (2a)^2 - 4*3*[-(a^2-8a)]
#            = 4a^2 + 12(a^2-8a)
#            = 16a^2 - 96a
#            = 16a(a-6)

a = symbols('a', real=True)
D = 16*a**2 - 96*a

a_candidate = int(CANDIDATE)

# 검증 1: a = CANDIDATE일 때 D <= 0
D_at_candidate = D.subs(a, a_candidate)
check1 = (D_at_candidate <= 0)

# 검증 2: a > CANDIDATE일 때 D > 0 (최댓값임을 확인)
D_at_larger = D.subs(a, a_candidate + 0.01)
check2 = (D_at_larger > 0)

# 검증 3: 범위 내 a (예: a=5)에서 D <= 0
D_at_inside_range = D.subs(a, a_candidate - 1)
check3 = (D_at_inside_range <= 0)

if check1 and check2 and check3:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")