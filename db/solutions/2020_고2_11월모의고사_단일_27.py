import sympy as sp
from sympy import cos, sin, tan, sqrt, symbols, solve, simplify

CANDIDATE = 20

theta = symbols('theta', real=True)

# 근의 합 = 0 조건
eq1 = 6*cos(theta) + 5*tan(theta)

# 근의 곱 = -k 조건
root_product = 6*cos(theta) * 5*tan(theta)

# sin(theta)에 대한 방정식 풀기
eq_sin = 6*cos(theta)**2 + 5*sin(theta)
eq_substituted = 6*(1 - sin(theta)**2) + 5*sin(theta)
sin_solutions = solve(eq_substituted, sin(theta))

# sin(theta) = -2/3인 경우
sin_val = -sp.Rational(2, 3)
cos_sq = 1 - sin_val**2
cos_sq_val = sp.Rational(5, 9)

# 확인: 6*cos^2(theta) + 5*sin(theta) = 0
check_sum = 6*cos_sq_val + 5*sin_val
if check_sum == 0:
    # 두 근 계산
    cos_val = sqrt(sp.Rational(5, 9))
    tan_val = sin_val / cos_val
    
    root1 = 6*cos_val
    root2 = 5*tan_val
    
    # 근과 계수 확인
    root_sum = simplify(root1 + root2)
    root_prod = simplify(root1 * root2)
    k_calculated = -root_prod
    
    if simplify(root_sum) == 0 and k_calculated == CANDIDATE:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')