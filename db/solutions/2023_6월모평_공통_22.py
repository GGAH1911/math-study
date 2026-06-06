from fractions import Fraction
import sympy as sp
from sympy import symbols, sqrt, Abs, limit, oo, piecewise_fold

CANDIDATE = 19

# 문제의 원래 조건에서 유도되는 값들
a = Fraction(3, 4)
b = 9
# f(x) = (x+3)^2 (최고차항의 계수가 1인 이차함수)

# 검증 1: g(x) 정의 및 연속성 검증
# x < 0: g(x) = (x+3)f(x) = (x+3)(x+3)^2 = (x+3)^3
# x >= 0: g(x) = (x+a)f(x-b) = (x+3/4)(x-9+3)^2 = (x+3/4)(x-6)^2

# x -> 0^-에서의 좌극한
g_left_limit = (0 + 3)**3  # = 27

# x = 0에서의 값
g_0 = (0 + a) * (0 - 6)**2  # = (3/4) * 36 = 27

assert g_left_limit == g_0, f"연속성 실패: {g_left_limit} != {g_0}"

# 검증 2: 영점 찾기
# x < 0에서 g(x) = (x+3)^3 = 0 => x = -3
# x >= 0에서 g(x) = (x+3/4)(x-6)^2 = 0 => x = -3/4 (< 0, 범위 밖) 또는 x = 6

zeros_at = {-3, 6}  # 전체 영점

# 검증 3: 극한 조건 검증
# x < 0에서 g(x) = (x+3)^3이고, x -> -3으로 접근할 때
# 극한: lim_{x->-3} [sqrt(|g(x)|+g(t)^2) - |g(t)|] / (x+3)^2
# 
# 분자 유리화:
# = |g(x)| / [(x+3)^2 * (sqrt(|g(x)|+g(t)^2) + |g(t)|)]
# = |(x+3)^3| / [(x+3)^2 * (sqrt(|(x+3)^3|+g(t)^2) + |g(t)|)]
# = |x+3| / [sqrt(|(x+3)^3|+g(t)^2) + |g(t)|]
#
# h = x+3 -> 0^-일 때:
# = |h| / [sqrt(|h|^3+g(t)^2) + |g(t)|]
#
# g(t) = 0인 경우:
#   = |h| / sqrt(|h|^3) = |h| / |h|^(3/2) = 1/|h|^(1/2) -> +infinity (극한 불존재)
#
# g(t) != 0인 경우:
#   = |h| / [sqrt(g(t)^2) + |g(t)|] -> 0 / [2|g(t)|] = 0 (극한 존재)
#
# 따라서 극한이 존재하지 않는 t <=> g(t) = 0 <=> t ∈ {-3, 6}

# 검증 4: g(4) 계산
# x = 4 >= 0이므로:
# g(4) = (4 + 3/4) * (4 - 6)^2
#      = (19/4) * (-2)^2
#      = (19/4) * 4
#      = 19

g_4 = (4 + a) * (4 - 6)**2

assert g_4 == CANDIDATE, f"g(4) 불일치: {g_4} != {CANDIDATE}"

# 검증 5: 모든 조건 최종 확인
assert a == Fraction(3, 4), f"a 값 오류"
assert b == 9, f"b 값 오류"
assert b > 3, f"b > 3 조건 실패"
assert g_left_limit == g_0, f"연속성 실패"
assert zeros_at == {-3, 6}, f"영점 조건 실패: {zeros_at}"
assert g_4 == 19, f"g(4) = 19 조건 실패"

print("VERIFY_PASS")