import sympy as sp
import numpy as np
from sympy import sqrt, simplify

# 주어진 답
sin_theta1 = sqrt(5) / 5

# tan θ₁ = 1/2일 때 sin θ₁의 값 검증
# tan θ₁ = 1/2이고 θ₁ ∈ (0, π/2)일 때
# sin θ₁ = tan θ₁ / √(1 + tan²θ₁)
tan_theta1 = sp.Rational(1, 2)
sin_expected = tan_theta1 / sqrt(1 + tan_theta1**2)
sin_expected = simplify(sin_expected)

# 답이 맞는지 확인
if simplify(sin_theta1 - sin_expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')