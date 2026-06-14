import sympy as sp
from sympy import sqrt, simplify, cos, sin, pi

CANDIDATE = (6 - sqrt(6)) / 5

r = CANDIDATE

# 좌표 설정
# A = (0, r), B = (-r*sqrt(3)/2, -r/2), C = (r*sqrt(3)/2, -r/2)
# D = (r*cos(phi), r*sin(phi))

# BD = sqrt(2) 조건에서 phi 구하기
phi = sp.Symbol('phi', real=True)
BD_squared = (r*cos(phi) + r*sqrt(3)/2)**2 + (r*sin(phi) + r/2)**2
BD_eq = BD_squared - 2

# sin(theta) = sqrt(3)/3에서 나오는 sin(phi) 값
sin_phi_from_theta = sqrt(6)/(3*r) - sp.Rational(1,2)
cos_phi_from_theta = 2*sqrt(3)/(3*r) - sqrt(3)/2

# sin²φ + cos²φ = 1 확인
identity_check = simplify(sin_phi_from_theta**2 + cos_phi_from_theta**2 - 1)

if simplify(identity_check) == 0:
    # BD = sqrt(2) 확인
    BD_value = sqrt((r*cos_phi_from_theta + r*sqrt(3)/2)**2 + (r*sin_phi_from_theta + r/2)**2)
    BD_simplified = simplify(BD_value)
    
    # sin(theta) 확인
    BC_vec = (r*sqrt(3), 0)
    BD_vec = (r*cos_phi_from_theta + r*sqrt(3)/2, r*sin_phi_from_theta + r/2)
    cross_product = BC_vec[0]*BD_vec[1] - BC_vec[1]*BD_vec[0]
    sin_theta_calc = simplify(cross_product / (r*sqrt(3) * sqrt(2)))
    
    if simplify(BD_simplified - sqrt(2)) == 0 and simplify(sin_theta_calc - sqrt(3)/3) == 0:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')