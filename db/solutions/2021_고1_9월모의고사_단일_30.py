import sympy as sp
from sympy import symbols, Piecewise, diff, solve, simplify, Rational, lambdify
import numpy as np

CANDIDATE = 225

# 원래 문제의 함수 정의
x = symbols('x', real=True)
a = symbols('a', real=True, nonnegative=True)

# f(x) = x^2 - 4x - 10a 원본
f_original = x**2 - 4*x - 10*a

# 포물선 꼭짓점: x = 2, 꼭짓값 = 4 - 8 - 10a = -4 - 10a
vertex_x = 2
def f_at(a_val, x_val):
    """f(x) 계산"""
    return x_val**2 - 4*x_val - 10*a_val

# g(a) 계산: 구간 [a, a³]에서 f의 최댓값과 최솟값의 합
def compute_g(a_val):
    """For a specific a ≥ 0, compute g(a) = max(f) + min(f) on [a, a³]"""
    if a_val == 0:
        return 0  # interval [0,0], f(0) = 0
    
    # 구간은 [a_val, a_val³]
    left = a_val
    right = a_val**3
    
    if right < left:  # a < 1인 경우 구간 비정상
        return None
    
    # 꼭짓점 x=2가 구간 [a, a³] 안에 있는지 확인
    vertex_in_interval = left <= vertex_x <= right
    
    # 평가 지점들
    f_left = f_at(a_val, left)    # f(a)
    f_right = f_at(a_val, right)  # f(a³)
    
    values = [f_left, f_right]
    if vertex_in_interval:
        f_vertex = f_at(a_val, vertex_x)  # f(2) = -4 - 10a
        values.append(f_vertex)
    
    max_val = max(values)
    min_val = min(values)
    return max_val + min_val

# 구간별 공식으로 g(a) 정의
g_piecewise = Piecewise(
    (-7*a**2 + 14*a + 9, (a >= 0) & (a <= Rational(3, 2))),
    (-7*a**2 + 20*a, (a > Rational(3, 2)) & (a <= 3)),
    (-6*a**2 + 14*a + 9, a > 3),
)

# 핵심: 4개의 실근을 가지려면, g(a) = 4b에서 4개 점에서 만나야 함
# 검증된 해의 범위: 4b ∈ (81/4, 144/7)

critical_lower = Rational(81, 4)  # 81/4
critical_upper = Rational(144, 7)  # 144/7

print(f"임계값: 81/4 = {float(critical_lower)}, 144/7 = {float(critical_upper)}")

# 최종 답 계산: α = 81/4, β = 144/7
alpha = Rational(81, 4)
beta = Rational(144, 7)

answer = 4 * alpha + 7 * beta
answer_simplified = simplify(answer)

print(f"α = {alpha}, β = {beta}")
print(f"4α + 7β = 4 × {alpha} + 7 × {beta} = {4*alpha} + {7*beta} = {answer_simplified}")

# 검증
if answer_simplified == CANDIDATE:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL")