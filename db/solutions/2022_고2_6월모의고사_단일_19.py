from sympy import *

CANDIDATE = 1

# 문제 기하학 설정
theta = symbols('theta', real=True, positive=True)

# 호 AB의 삼등분점 C (A에 가까움)
# A에서 시작해 호의 θ/3만큼 이동 → C
# ∠AOC = θ/3, ∠AOB = θ
# 따라서 ∠BOC = θ - θ/3 = 2θ/3
angle_BOC = 2*theta/3

# (가) = ∠BOC
f = lambda t: 2*t/3

# 삼각형 BOC: OB = OC = 1 (반지름), ∠BOC = 2θ/3
# 이등변삼각형: ∠OBC = ∠OCB = (π - 2θ/3)/2
angle_OBC = (pi - 2*theta/3) / 2

# 삼각형 BOD의 사인법칙
# D는 직선 OA와 직선 BC의 교점
# ∠BOD = θ (D가 OA 연장선상)
# ∠DBO = ∠OBC = (π - 2θ/3)/2
# ∠BDO = π - θ - (π - 2θ/3)/2 = π/2 - 2θ/3
angle_BDO = pi/2 - 2*theta/3

# 사인법칙: OD/sin(∠DBO) = OB/sin(∠BDO)
# OD = sin((π - 2θ/3)/2) / sin(π/2 - 2θ/3)
# sin((π - 2θ/3)/2) = cos(θ/3)
# sin(π/2 - 2θ/3) = cos(2θ/3)
# OD = cos(θ/3) / cos(2θ/3)

# (나) = cos(2θ/3)
g = lambda t: cos(2*t/3)

# S(θ): 선분 AD, CD와 호 AC로 둘러싸인 넓이
# = 삼각형 COD의 넓이 - 부채꼴 OAC의 넓이

# 삼각형 COD
# OC = 1, OD = cos(θ/3)/cos(2θ/3), ∠COD = θ/3 (∠AOC와 같음, D가 OA 연장선상)
# 넓이 = (1/2) × OC × OD × sin(∠COD)
#      = (1/2) × 1 × [cos(θ/3)/cos(2θ/3)] × sin(θ/3)
#      = (1/2) × cos(θ/3) × sin(θ/3) / cos(2θ/3)

OD_expr = cos(theta/3) / cos(2*theta/3)
area_COD = Rational(1,2) * OD_expr * sin(theta/3)
area_COD_simplified = simplify(area_COD)

# 부채꼴 OAC: 반지름 1, 중심각 θ/3
# 넓이 = (1/2) × 1² × (θ/3) = θ/6
area_sector_OAC = theta / 6

# S(θ) = area_COD - area_sector_OAC
S_expr = area_COD_simplified - area_sector_OAC
S_simplified = simplify(S_expr)

# 문제: S(θ) = (1/2) × cos(θ/3) / (나) × sin(θ/3) - (다)
# (다) = θ/6
h = lambda t: t/6

# 최종 계산: f(π/2) × g(π/4) / h(π/8)
pi_sym = pi
f_pi_2 = f(pi_sym/2)          # = π/3
g_pi_4 = g(pi_sym/4)          # = cos(π/6) = √3/2
h_pi_8 = h(pi_sym/8)          # = π/48

result = f_pi_2 * g_pi_4 / h_pi_8
result_simplified = simplify(result)

# 문제의 보기
options = {
    1: 8*sqrt(3),
    2: 17*sqrt(3)/2,
    3: 9*sqrt(3),
    4: 19*sqrt(3)/2,
    5: 10*sqrt(3)
}

# 검증: CANDIDATE 보기의 값이 계산 결과와 같은가
if CANDIDATE in options:
    candidate_value = options[CANDIDATE]
    difference = simplify(result_simplified - candidate_value)
    if difference == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')