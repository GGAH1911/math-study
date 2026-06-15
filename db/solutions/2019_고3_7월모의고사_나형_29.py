CANDIDATE = 273

# 등차수열 검증
import sympy as sp
from fractions import Fraction

# a = -13d 조건 확인
d = sp.Symbol('d', real=True, nonzero=True)
a = -13 * d

# S_9 = S_18 확인
S_9 = 9*a + 9*8*d/2
S_18 = 18*a + 18*17*d/2
assert sp.simplify(S_9 - S_18) == 0, "S_9 = S_18 조건 실패"

# f(k) = k(k-27) 값들 계산
def f(k):
    return k * (k - 27)

# k=1부터 26까지 f(k) 값의 서로 다른 개수
values_1_to_26 = set()
for k in range(1, 27):
    values_1_to_26.add(f(k))

assert len(values_1_to_26) == 13, f"1~26에서 서로 다른 값은 {len(values_1_to_26)}개, 13개여야 함"

# 대칭성 확인: f(k) = f(27-k) for k=1...13
for k in range(1, 14):
    assert f(k) == f(27-k), f"f({k}) != f({27-k})"

# f(27) = 0
assert f(27) == 0, "f(27) != 0"

# f(28), f(29) 등은 새로운 양수값
f_28 = f(28)  # = 28
f_29 = f(29)  # = 58
assert f_28 == 28 and f_29 == 58, "f(28), f(29) 값 오류"
assert f_28 not in values_1_to_26, "f(28)이 이미 있는 값"

# |T_n| 계산
def count_T_n(n):
    values = set()
    for k in range(1, n+1):
        values.add(f(k))
    return len(values)

# n=13부터 26까지 |T_n|=13 확인
valid_n = []
for n in range(1, 40):
    if count_T_n(n) == 13:
        valid_n.append(n)

assert valid_n == list(range(13, 27)), f"|T_n|=13인 n: {valid_n}"

# 합 계산
total = sum(range(13, 27))
assert total == CANDIDATE, f"합 {total} != {CANDIDATE}"

print("VERIFY_PASS")