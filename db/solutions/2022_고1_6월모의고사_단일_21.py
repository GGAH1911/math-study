import numpy as np
from fractions import Fraction

def f_min(a, b):
    # 원 함수 f(x)=(x-a)^2 + b 의 [1,2] 최솟값 (수치)
    xs = np.linspace(1, 2, 200001)
    return float(np.min((xs - a)**2 + b))

# ---- ㄱ: a=3/2 일 때 b=5 ----
stmt_g = abs(f_min(1.5, 5.0) - 5.0) < 1e-9

# ---- ㄴ: a<=1 일 때 b = -a^2+2a+4 가 최솟값=5 만족 ----
stmt_n = True
for a in np.linspace(-5.0, 1.0, 121):
    b = -a*a + 2*a + 4
    if abs(f_min(a, b) - 5.0) > 1e-6:
        stmt_n = False
        break

# ---- ㄷ: 최솟값=5 조건 하에서 a+b의 최댓값 = 29/4 ----
# a 위치에 따른 b(a) 구성
def b_from_a(a):
    if a < 1:
        return 5 - (1 - a)**2
    elif a <= 2:
        return 5.0
    else:
        return 5 - (2 - a)**2

A = np.linspace(-20, 20, 400001)
vals = np.array([a + b_from_a(a) for a in A])
# 검증: 각 (a, b_from_a(a))가 실제로 최솟값=5를 만족하는지
ok_constraint = all(abs(f_min(a, b_from_a(a)) - 5.0) < 1e-6 for a in [-3, 0, 0.5, 1, 1.5, 2, 2.5, 3, 4])
max_ab = float(vals.max())
stmt_d = ok_constraint and abs(max_ab - 29.0/4.0) < 1e-3

my_answer = 5  # ㄱ, ㄴ, ㄷ
expected_set = (stmt_g, stmt_n, stmt_d)
# 답안 선택지 매핑
mapping = {
    (True, False, False): 1,
    (True, True, False): 2,
    (True, False, True): 3,
    (False, True, True): 4,
    (True, True, True): 5,
}
computed = mapping.get(expected_set, -1)
print('VERIFY_PASS' if computed == my_answer else 'VERIFY_FAIL')
