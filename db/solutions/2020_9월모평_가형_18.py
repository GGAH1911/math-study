from sympy import Rational, simplify

CANDIDATE = 2

# 주어진 확률 값
# (가): (6,1,2)와 (6,2,1) 각각 C(6,6)*C(3,1)*C(3,2) / C(12,9)
p = Rational(9, 220)

# (나): (6,2,2) - 처음 9개 (5,2,2) 선택 후 10번째 빨강
q = Rational(9, 110)

# 핵심 관계식: p + q = ?
result = p + q

# 선택지 (객관식 보기)
choices = [
    Rational(13, 110),   # ①
    Rational(27, 220),   # ②
    Rational(7, 55),     # ③
    Rational(29, 220),   # ④
    Rational(3, 22),     # ⑤
]

# CANDIDATE(=2번 선택지)와 비교
expected = choices[CANDIDATE - 1]

# 검증: 계산된 p+q가 정답과 일치하는지
if simplify(result - expected) == 0:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")