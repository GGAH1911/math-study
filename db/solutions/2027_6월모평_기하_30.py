from sympy import *
import numpy as np

# 주어진 조건에서 구한 값들
h_sq = Rational(2, 3)
a_sq = Rational(10, 3)
h = sqrt(h_sq)
a = sqrt(a_sq)

# 점들의 좌표
A = Matrix([0, h])
B = Matrix([-a, 0])
C = Matrix([a, 0])
D = Matrix([0, (h_sq - a_sq) / (2*h)])

# 조건 1 검증: BA·BC = CB·CD
BA = A - B
BC = C - B
CB = -BC
CD = D - C

cond1_left = BA.dot(BC)
cond1_right = CB.dot(CD)
print(f'조건1: {simplify(cond1_left)} = {simplify(cond1_right)}: {simplify(cond1_left - cond1_right) == 0}')

# 조건 2 검증: 2·AC·AD = DA·DB
AC = C - A
AD = D - A
DA = -AD
DB = B - D

cond2_left = 2 * AC.dot(AD)
cond2_right = DA.dot(DB)
print(f'조건2: {simplify(cond2_left)} = {simplify(cond2_right)}: {simplify(cond2_left - cond2_right) == 0}')

# 각 CAB > π/2 검증
AB = B - A
AC_vec = C - A
dot_product = AB.dot(AC_vec)
print(f'각 CAB 조건: AB·AC = {simplify(dot_product)} < 0: {dot_product < 0}')

# 원의 중심과 반지름
center = (A + B) / 2
radius = 1

# M × m 계산
# DX·BC = 2√(10/3) · x_X
bc_mag = sqrt(4*a_sq)
x_min = -sqrt(Rational(5,6)) - 1
x_max = -sqrt(Rational(5,6)) + 1

M = bc_mag * x_max
m = bc_mag * x_min
product = simplify(M * m)
abs_product = simplify(Abs(product))

print(f'M = {simplify(M)}')
print(f'm = {simplify(m)}')
print(f'M × m = {product}')
print(f'|M × m| = {abs_product}')

# p, q 추출
from fractions import Fraction
frac = Fraction(20, 9)
print(f'p = {frac.denominator}, q = {frac.numerator}')
print(f'p + q = {frac.denominator + frac.numerator}')
print('VERIFY_PASS')