"""Verifier for 2020_6월모평_가형_22.

Problem: 벡터 a = (2, 1)에 대하여 벡터 10a의 모든 성분의 합을 구하시오.
Derive: 10*a = 10*(2,1) = (20,10); sum of components = 30.
"""
from sympy import Rational, Matrix

CANDIDATE = 30

# Original problem data: vector a = (2, 1), scalar multiple 10.
a = Matrix([Rational(2), Rational(1)])
scalar = Rational(10)

# 벡터의 스칼라배: 10 * a, applied component-wise.
ten_a = scalar * a

# 모든 성분의 합 (sum of all components of 10a).
components_sum = sum(ten_a)

if components_sum == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")
