from sympy import *
from fractions import Fraction
import math

CANDIDATE = 17

# ============================================================
# 타원 정의: x²/9 + y²/5 = 1
# ============================================================
a_sq = 9       # a² = 9, a = 3
b_sq = 5       # b² = 5, b = √5
c_sq = a_sq - b_sq  # c² = 4, c = 2

# 초점
F = (2, 0)     # 우측 초점 (c, 0)
Fp = (-2, 0)   # 좌측 초점 (-c, 0)

# 원의 중심과 반지름
C = (2, 3)  # 원의 중심
r = CANDIDATE  # 원의 반지름

# ============================================================
# 검증 1: 타원의 성질 확인
# 타원 위의 임의 점 P에 대해 |PF| + |PF'| = 2a = 6
# ============================================================
print("[검증 1] 타원 정의: |PF| + |PF'| = 6")

test_angles = [0, pi/6, pi/4, pi/3, pi/2, 2*pi/3, 3*pi/4, 5*pi/6, pi]
ellipse_verified = True

for theta in test_angles:
    P_x = 3*cos(theta)
    P_y = sqrt(5)*sin(theta)
    
    # |PF| 계산
    dist_F = sqrt((P_x - F[0])**2 + (P_y - F[1])**2)
    # |PF'| 계산
    dist_Fp = sqrt((P_x - Fp[0])**2 + (P_y - Fp[1])**2)
    
    sum_dist = simplify(dist_F + dist_Fp)
    
    if simplify(sum_dist - 6) != 0:
        ellipse_verified = False
        print(f"  ✗ Failed at θ={theta}")

if ellipse_verified:
    print(f"  ✓ 모든 타원 위의 점에서 |PF| + |PF'| = 6")

# ============================================================
# 검증 2: |F'C| = 5 확인
# ============================================================
print("\n[검증 2] 초점 F'과 원의 중심 C 사이 거리")
dist_FpC = sqrt((C[0] - Fp[0])**2 + (C[1] - Fp[1])**2)
dist_FpC_simplified = simplify(dist_FpC)
print(f"  |F'C| = {dist_FpC_simplified}")

if dist_FpC_simplified == 5:
    print(f"  ✓ |F'C| = 5 확인됨")
else:
    print(f"  ✗ |F'C| ≠ 5")

# ============================================================
# 검증 3: 핵심 점 P 찾기 (직선 F'C와 타원의 교점)
# 직선 F'C 위의 점: (-2 + 4t, 3t)
# 타원식 대입: ((-2+4t)²)/9 + (3t)²/5 = 1
# ============================================================
print("\n[검증 3] 직선 F'C와 타원의 교점")

t = symbols('t', real=True)
ellipse_eq = ((-2 + 4*t)**2)/9 + (3*t)**2/5 - 1
t_solutions = solve(ellipse_eq, t)
print(f"  방정식의 해: {t_solutions}")

# 대상 t값
t_target = Rational(-35, 161)
print(f"  목표 t = {t_target}")

if t_target in t_solutions:
    print(f"  ✓ t = -35/161은 방정식의 해")
    
    # 이 t에 대한 점 P의 좌표
    P_x = -2 + 4*t_target
    P_y = 3*t_target
    P = (P_x, P_y)
    
    print(f"  교점 P = ({P_x}, {P_y})")
    
    # P가 타원 위에 있는지 확인
    ellipse_check = simplify(P_x**2/9 + P_y**2/5)
    print(f"  x²/9 + y²/5 = {ellipse_check} (타원 위: {ellipse_check == 1})")
    
    # |PF'|과 |PC| 계산
    dist_PFp = sqrt((P_x - Fp[0])**2 + (P_y - Fp[1])**2)
    dist_PC = sqrt((P_x - C[0])**2 + (P_y - C[1])**2)
    
    dist_PFp_simplified = simplify(dist_PFp)
    dist_PC_simplified = simplify(dist_PC)
    
    print(f"  |PF'| = {dist_PFp_simplified}")
    print(f"  |PC| = {dist_PC_simplified}")
    
    # |PF'| - |PC| 계산 (역삼각부등식의 등호 조건)
    diff = simplify(dist_PFp - dist_PC)
    print(f"  |PF'| - |PC| = {diff}")
    
    if diff == -5:
        print(f"  ✓ |PF'| - |PC| = -5 (역삼각부등식 등호 성립)")

# ============================================================
# 검증 4: 최솟값 조건 확인
# 논리:
#   PQ - PF = PQ + PF' - (PF + PF') = PQ + PF' - 6
#   min(PQ - PF) = min(PQ + PF') - 6
#   
#   원이 타원을 포함 ⟹ min(PQ) = r - |PC|
#   min(PQ + PF') = r + min(|PF'| - |PC|)
#   역삼각부등식: |PF'| - |PC| ≥ -|F'C| = -5
#   따라서: min(PQ + PF') = r - 5
#   
#   min(PQ - PF) = (r - 5) - 6 = r - 11
#   조건: r - 11 = 6 ⟹ r = 17
# ============================================================
print("\n[검증 4] 최솟값 조건")
print(f"  주어진 조건: min(PQ - PF) = 6")
print(f"  \n  도출 과정:")
print(f"  PQ - PF = PQ + PF' - 6")
print(f"  min(PQ + PF') = r + min(|PF'| - |PC|)")
print(f"  역삼각부등식에 의해 min(|PF'| - |PC|) = -|F'C| = -5")
print(f"  따라서 min(PQ + PF') = {r} - 5 = {r - 5}")
print(f"  \n  min(PQ - PF) = min(PQ + PF') - 6")
print(f"             = {r - 5} - 6")
print(f"             = {r - 11}")
print(f"  \n  조건 검증: {r - 11} = 6 ?")

if r - 11 == 6:
    print(f"  ✓ r = {r}일 때 min(PQ - PF) = 6 성립")
    print(f"\n" + "="*60)
    print("VERIFY_PASS")
    print("="*60)
else:
    print(f"  ✗ {r - 11} ≠ 6")
    print(f"\n" + "="*60)
    print("VERIFY_FAIL")
    print("="*60)