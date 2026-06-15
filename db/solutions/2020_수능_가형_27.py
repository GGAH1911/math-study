import numpy as np
from scipy.optimize import fsolve
import sympy as sp

CANDIDATE = 8

# 마름모의 꼭짓점
A_flat = np.array([0, 0])
B_flat = np.array([4, 0])
D_flat = np.array([2, 2*np.sqrt(3)])
C_flat = np.array([6, 2*np.sqrt(3)])

# M, N
M_flat = (B_flat + C_flat) / 2
N_flat = (C_flat + D_flat) / 2

# 3D 좌표
A = np.array([0, 0, 0])
M = np.array([2*np.sqrt(7), 0, 0])
N = np.array([13*np.sqrt(7)/7, 3*np.sqrt(21)/7, 0])

# P의 좌표
P = np.array([10*np.sqrt(7)/7, 10*np.sqrt(21)/63, 4*np.sqrt(6)/9])

# 거리 검증
dist_AP = np.linalg.norm(P - A)
dist_PM = np.linalg.norm(P - M)
dist_PN = np.linalg.norm(P - N)

assert np.isclose(dist_AP, 4), f"AP 거리 오류: {dist_AP}"
assert np.isclose(dist_PM, 2), f"PM 거리 오류: {dist_PM}"
assert np.isclose(dist_PN, 2), f"PN 거리 오류: {dist_PN}"

# 삼각형 AMN의 넓이
AM = M - A
AN = N - A
cross_product = np.cross(AM, AN)
area_AMN = 0.5 * np.linalg.norm(cross_product)

# 평면 PAM의 법선
AP = P - A
normal_PAM = np.cross(AM, AP)

# 평면 AMN의 법선 (z축)
normal_AMN = np.array([0, 0, 1])

# 두 평면 사이의 각도
cos_theta = np.abs(np.dot(normal_AMN, normal_PAM)) / (np.linalg.norm(normal_PAM))

# 정사영 넓이
area_projection = area_AMN * cos_theta

# (q/p)*sqrt(3) 형태에서 q/p 추출
coeff = area_projection / np.sqrt(3)

# p, q 계산 (q/p = coeff)
from fractions import Fraction
frac = Fraction(coeff).limit_denominator(1000)
q_computed = frac.numerator
p_computed = frac.denominator

answer_computed = p_computed + q_computed

if answer_computed == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')