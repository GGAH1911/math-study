import sympy as sp
from sympy import pi, cos, sin, simplify, Rational

CANDIDATE = 125

# ========== 문제 조건 분석 ==========
# f'(x) = |sin(x)| * cos(x)
# h'(x) = f(x) - f(a) - f'(a)*(x-a), h'(a)=0
# h'가 x=a에서 극값 조건: h'(x) ≈ (f''(a)/2)*(x-a)^2 + (f'''(a)/6)*(x-a)^3
#
# 극값 조건 1: f''(a)=0 이고 f'''(a)≠0
# 극값 조건 2: a=kπ (k≥1) 특수경우

# ========== f''(x), f'''(x) 구간별 계산 ==========
# (0, π): sin(x) > 0 → f'(x) = sin(x)*cos(x)
#         f''(x) = cos(2x)
#         f'''(x) = -2*sin(2x)
#
# (π, 2π): sin(x) < 0 → f'(x) = -sin(x)*cos(x)
#          f''(x) = -cos(2x)
#          f'''(x) = 2*sin(2x)

# ========== 극값점 찾기 ==========
# f''(a) = 0 조건: cos(2a) = 0 → a = π/4 + nπ/2
# 후보: a = π/4, 3π/4, 5π/4, 7π/4, ...

# 검증: 각 점에서 f'''(a)≠0 확인
extreme_points = []

# a = π/4 (구간 (0,π))
a = pi/4
f_triple = -2*sin(2*a)  # -2*sin(π/2) = -2
if f_triple != 0:
    extreme_points.append(a)  # ✓ a_1

# a = 3π/4 (구간 (0,π))
a = 3*pi/4
f_triple = -2*sin(2*a)  # -2*sin(3π/2) = 2
if f_triple != 0:
    extreme_points.append(a)  # ✓ a_2

# a = 5π/4 (구간 (π,2π))
a = 5*pi/4
f_triple = 2*sin(2*a)  # 2*sin(5π/2) = 2
if f_triple != 0:
    extreme_points.append(a)  # ✓ a_4

# a = 7π/4 (구간 (π,2π))
a = 7*pi/4
f_triple = 2*sin(2*a)  # 2*sin(7π/2) = -2
if f_triple != 0:
    extreme_points.append(a)  # ✓ a_5

# 특수경우: a = kπ (k≥1)
# f'(kπ)=0이고 구간경계에서 부호변화 → 극값
for k in range(1, 3):
    extreme_points.append(k*pi)

# 정렬
extreme_points.sort()

# 검증: 최소 6개 이상의 극값점 필요
assert len(extreme_points) >= 6, f"found only {len(extreme_points)} extrema"

# a_2, a_6 추출
a_2 = extreme_points[1]  # 3π/4
a_6 = extreme_points[5]  # 2π

# ========== 최종 계산 ==========
difference = a_6 - a_2
# 2π - 3π/4 = 8π/4 - 3π/4 = 5π/4

difference_simplified = simplify(difference)
assert difference_simplified == 5*pi/4, f"difference mismatch: {difference_simplified}"

result = Rational(100) * difference / pi
# (100/π) * (5π/4) = 100*5/4 = 125

result_simplified = simplify(result)

# ========== 검증 ==========
if result_simplified == CANDIDATE:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL")