import sympy as sp
from sympy import log, solve, simplify

CANDIDATE = 16

# k를 구하기 위해 역계산
k_cubed = CANDIDATE
k = k_cubed ** (1/3)

# log_2(k) 계산
t = log(k, 2)
print(f"log_2(k) = {t}")
print(f"Numerical: {float(t)}")

# 교점 좌표
x_A = 1 - t
x_B = 1 + t/2

print(f"x_A = {x_A}")
print(f"x_B = {x_B}")

# 거리
AC = -x_A  # x_A < 0이므로
CB = x_B   # x_B > 0

print(f"AC = {AC}")
print(f"CB = {CB}")

# 비율 확인
ratio = simplify(AC / CB)
print(f"AC/CB = {ratio}")
print(f"Numerical: {float(AC/CB)}")

# 비율이 1/5인지 확인
if abs(float(AC/CB) - 0.2) < 1e-9:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")