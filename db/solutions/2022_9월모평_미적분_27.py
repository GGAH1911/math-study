from sympy import sqrt, simplify, fraction, Rational

CANDIDATE = 3

# 직사각형 좌표: A(0,1), B₁(0,0), C₁(2,0), D₁(2,1)
# AB₁ = 1, B₁C₁ = 2

# 첫 번째 단계: S₁ 계산
# 검증된 풀이에서:
# E₁F₁ = 2√3/3
# S₁ = (6-√3)/9 (삼각형 G₁E₁H₁과 H₁F₁D₁의 넓이 합)
S1 = (6 - sqrt(3)) / 9

# 닮음비 r = 1 - √3/3
r = 1 - sqrt(3) / 3

# 기하급수의 합: lim S_n = S₁ / (1 - r²)
# 1 - r² 계산
one_minus_r2 = 1 - r**2
one_minus_r2_simplified = simplify(one_minus_r2)
# 검증: 1 - r² = (2√3 - 1) / 3
expected_one_minus_r2 = (2*sqrt(3) - 1) / 3
assert simplify(one_minus_r2_simplified - expected_one_minus_r2) == 0

# 극한값 계산
limit_an = simplify(S1 / one_minus_r2_simplified)

# 기약분수로 표현
# limit_an = √3/3 (분자=√3, 분모=3)
num, denom = fraction(limit_an)

# 극한값이 (√3)/3 형태임을 확인
expected_limit = sqrt(3) / 3
assert simplify(limit_an - expected_limit) == 0

# CANDIDATE는 극한값의 분모 (기약분수 표현에서)
if denom == CANDIDATE:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")