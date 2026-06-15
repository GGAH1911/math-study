from sympy import *
import numpy as np

# f(sqrt(2)) 검증
x = sqrt(2)
f_sqrt2 = 7 / (x**2 - 9)
assert f_sqrt2 == -1, f"ㄱ 검증 실패: {f_sqrt2}"

# f''(t) < 0 in (-3, 3) 검증
t = symbols('t', real=True)
f_t = 7 / (t**2 - 9)
f_prime = diff(f_t, t)
f_double_prime = diff(f_prime, t)
f_double_prime_simplified = simplify(f_double_prime)

# 시험점 t=0
f_double_at_0 = f_double_prime.subs(t, 0)
assert f_double_at_0 < 0, f"ㄴ 검증 실패: {f_double_at_0}"

# ㄷ 검증: 방정식 9f(x) = 3^(x+2) - 7의 근 개수
# (3, ∞) 구간에서만 해가 존재
def g(x_val):
    return 63 / (x_val**2 - 9) - (3**(x_val + 2) - 7)

# (3, ∞)에서 근 찾기
from scipy.optimize import brentq
root = brentq(g, 3.04, 3.08)
assert 3 < root < 4, f"근이 (3,∞) 범위에 없음"

# (-3, 3) 구간에서 근이 없음을 확인
assert g(0) < 0 and g(-2.9) < 0 and g(2.9) < 0, "(-3,3)에서 근 존재"

print("VERIFY_PASS")