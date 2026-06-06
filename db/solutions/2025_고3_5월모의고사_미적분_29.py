import sympy as sp
from sympy import sin, cos, tan, pi, sqrt, diff, symbols, simplify

CANDIDATE = '45'

# 문제 좌표 설정: B=(0,0), A=(-√3,0), C=(0,2)
# BC를 지름으로 하는 반원 위의 점 P=(sin φ, 1-cos φ), φ∈(0,π]

phi = symbols('phi', real=True, positive=True)

# 조건 1: 기하학적 관계
# A=(-√3,0), B=(0,0), P=(sin φ, 1-cos φ)
# ∠BAP = θ일 때: tan θ = (1-cos φ)/(√3 + sin φ)
tan_angle_BAP = (1 - cos(phi)) / (sqrt(3) + sin(phi))

# 조건 2: θ = π/6일 때 φ = 2π/3인지 확인
phi_target = 2 * pi / 3
tan_theta_pi6 = tan(pi / 6)
tan_check = tan_angle_BAP.subs(phi, phi_target)
assert simplify(tan_check - tan_theta_pi6) == 0, "φ=2π/3 fails to satisfy tan condition"

# 조건 3: 삼각형 ABP의 넓이
# 밑변 AB = √3, 높이 = P의 y좌표 = 1-cos φ
# f(θ) = (√3/2)(1-cos φ(θ))
f_expr = (sqrt(3) / 2) * (1 - cos(phi))

# 조건 4: 음함수 미분으로 dφ/dθ 계산
# d(tan θ)/dφ를 먼저 구함
d_tan_angle = diff(tan_angle_BAP, phi)

# φ = 2π/3에서 평가
d_tan_angle_at_pi6 = simplify(d_tan_angle.subs(phi, phi_target))

# sec²(π/6) = 1/cos²(π/6) = 4/3
sec_sq_pi6 = simplify(1 / cos(pi/6)**2)

# dφ/dθ = sec²θ / [d(tan θ)/dφ]
d_phi_d_theta = simplify(sec_sq_pi6 / d_tan_angle_at_pi6)

# 조건 5: f'(θ) = (√3/2) sin φ(θ) · dφ/dθ
# θ = π/6 (φ = 2π/3)일 때:
sin_phi_at_pi6 = sin(phi_target)
f_prime_at_pi6 = simplify((sqrt(3) / 2) * sin_phi_at_pi6 * d_phi_d_theta)

# 최종 답: 20f'(π/6)
result = simplify(20 * f_prime_at_pi6)

# 검증
result_numeric = float(result)
candidate_numeric = float(CANDIDATE)

if abs(result_numeric - candidate_numeric) < 1e-10:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL")