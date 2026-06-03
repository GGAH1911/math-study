import numpy as np
from sympy import *

# 타원 방정식: x^2/8 + y^2 = 1
# P = (8/3, 1/3), Q = (-8/3, 1/3)

P = (Rational(8, 3), Rational(1, 3))
Q = (Rational(-8, 3), Rational(1, 3))

# P가 타원 위에 있는지 확인
x_p, y_p = P
ellipse_p = x_p**2 / 8 + y_p**2
print(f'P on ellipse: {ellipse_p} (should be 1)')
assert ellipse_p == 1, f'P not on ellipse: {ellipse_p}'

# Q가 타원 위에 있는지 확인
x_q, y_q = Q
ellipse_q = x_q**2 / 8 + y_q**2
print(f'Q on ellipse: {ellipse_q} (should be 1)')
assert ellipse_q == 1, f'Q not on ellipse: {ellipse_q}'

# A = (0, 3)에서 P로의 직선의 기울기
A = (0, 3)
m1 = (y_p - A[1]) / (x_p - A[0])
print(f'm1 = {m1}')

# A = (0, 3)에서 Q로의 직선의 기울기
m2 = (y_q - A[1]) / (x_q - A[0])
print(f'm2 = {m2}')

# 수직 조건 확인
product = m1 * m2
print(f'm1 * m2 = {product} (should be -1)')
assert product == -1, f'Lines not perpendicular: {product}'

# PQ의 길이 계산
length_PQ = sqrt((x_p - x_q)**2 + (y_p - y_q)**2)
print(f'|PQ| = {length_PQ} (should be 16/3)')
assert length_PQ == Rational(16, 3), f'Incorrect length: {length_PQ}'

print('VERIFY_PASS')