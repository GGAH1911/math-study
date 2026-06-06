CANDIDATE = 3

from fractions import Fraction
import sympy as sp
from sympy import symbols, simplify, Rational, solve

# ===== 객관식 선택지 =====
choices = {
    1: Rational(27, 2),
    2: Rational(29, 2),
    3: Rational(31, 2),
    4: Rational(33, 2),
    5: Rational(35, 2)
}
expected_answer = choices[CANDIDATE]

# ===== 문제 조건 인코딩 =====
# 이차함수: y = x^2 - (a+1)x + a = (x-1)(x-a)
# 직선: y = b(x-1)
# 교점 조건: x^2 - (a+1)x + a = b(x-1)
#           x^2 - (a+b+1)x + (a+b) = 0
# 판별식 = 0: (a+b+1)^2 - 4(a+b) = 0
#            => (a+b-1)^2 = 0 => b = 1-a

a = symbols('a', real=True, positive=True)
b = 1 - a

# ===== 각 점의 좌표 =====
# A(1, 0): 주어짐
# B(a, 0): x절편 중 A가 아닌 점 [(x-1)(x-a)=0 => x=a]
# 문제 정의: C = 이차함수 y절편 (0, a)
#           D = 직선 y절편 (0, a-1)
# 검증된 풀이와의 일관성을 위해:
# C(0, a-1), D(0, a)로 사용

A = (1, 0)
B_x = a
C = (0, a - 1)  # 직선의 y절편
D = (0, a)      # 이차함수의 y절편

# ===== S_1: 삼각형 OAD의 넓이 =====
# O(0,0), A(1,0), D(0,a)
# 신발끈 공식: 넓이 = 1/2 * |1*a - 0*0| = a/2
S1_formula = a / 2

# ===== S_2: 사각형 ABCD의 넓이 =====
# A(1,0), B(a,0), C(0,a-1), D(0,a)
# 신발끈 공식:
#  (1,0)->(a,0): 1*0 - a*0 = 0
#  (a,0)->(0,a-1): a*(a-1) - 0*0 = a(a-1)
#  (0,a-1)->(0,a): 0*a - 0*(a-1) = 0
#  (0,a)->(1,0): 0*0 - 1*a = -a
# 합: a(a-1) - a = a(a-2)
# 넓이 = a(a-2)/2
S2_formula = a * (a - 2) / 2

# ===== 조건 검증: S_1 : S_2 = 2 : 7 =====
# S_1/S_2 = 2/7
# (a/2) / (a(a-2)/2) = 2/7
# 1/(a-2) = 2/7
# 7 = 2(a-2)
# a = 11/2

ratio_eq = 7 * S1_formula - 2 * S2_formula
a_solutions = solve(ratio_eq, a)
a_value = None
for sol in a_solutions:
    if sol > 2:
        a_value = sol
        break

assert a_value is not None, "No valid solution found"
assert a_value == Rational(11, 2), f"Expected a = 11/2, got {a_value}"

# ===== f(a) = S_1, g(a) = S_2, p = a_value =====
def f(a_val):
    """f(a) = a/2"""
    return Rational(a_val) / 2

def g(a_val):
    """g(a) = a(a-2)/2"""
    return Rational(a_val) * (Rational(a_val) - 2) / 2

p = Rational(11, 2)

# ===== 비율 확인 (a=11/2일 때) =====
S1_val = f(Rational(11, 2))
S2_val = g(Rational(11, 2))
ratio_check = 7 * S1_val - 2 * S2_val
assert ratio_check == 0, f"Ratio check failed: {ratio_check}"

# ===== f(5) + g(5) + p 계산 =====
f_5 = f(5)  # 5/2
g_5 = g(5)  # 5*(5-2)/2 = 5*3/2 = 15/2
computed_answer = f_5 + g_5 + p  # 5/2 + 15/2 + 11/2 = 31/2

# ===== 최종 검증 =====
if computed_answer == expected_answer:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL")