import sympy as sp
from sympy import cos, sin, sqrt, acos, pi, simplify

# cos α = cos β = 1/3
cos_val = sp.Rational(1, 3)

# α는 제1사분면, β는 제4사분면
sin_alpha = sqrt(1 - cos_val**2)
sin_beta = -sqrt(1 - cos_val**2)

# sin(β - α) 계산
result = sin_beta * cos_val - cos_val * sin_alpha
result = simplify(result)

# 기댓값
expected = -4*sqrt(2)/9

if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')