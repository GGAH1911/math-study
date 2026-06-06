from sympy import symbols, discriminant, simplify, div
import sympy as sp

CANDIDATE = 15

# 원래 문제의 방정식
# x³ + 3x² + (16-a)x + a-20 = 0이 허근을 갖도록 하는 자연수 a의 개수

x, a = symbols('x a')
f = x**3 + 3*x**2 + (16 - a)*x + (a - 20)

# Step 1: x=1이 항상 근인지 확인 (a에 무관하게)
f_at_1 = simplify(f.subs(x, 1))
assert f_at_1 == 0, "x=1이 항상 근이 아닙니다"

# Step 2: (x-1)로 인수분해
quotient, remainder = div(f, x - 1)
assert remainder == 0, "인수분해 실패"
# quotient = x² + 4x + (20-a)

# Step 3: 이차식의 판별식 계산
disc = discriminant(quotient, x)
disc_simplified = simplify(disc)
# disc_simplified = 16 - 80 + 4a = 4a - 64

# Step 4: 허근을 갖기 위한 조건
# 판별식 < 0이면 이차식이 허근을 가짐
# 4a - 64 < 0
# a < 16

# Step 5: 자연수 a의 개수를 직접 셈
count = 0
for a_val in range(1, 100):
    disc_val = disc_simplified.subs(a, a_val)
    if disc_val < 0:  # 허근 조건 만족
        count += 1
    else:  # 조건 불만족, a가 증가하면서 disc도 증가하므로 이후 더 이상 조건을 만족하지 않음
        break

# CANDIDATE 검증
# 조건을 만족하는 자연수 a의 개수가 CANDIDATE와 일치해야 함
if count == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")