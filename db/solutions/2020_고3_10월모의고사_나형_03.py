from sympy import Rational, symbols, Eq, solve

CANDIDATE = 1  # 정답 선택지 번호

# 객관식 선택지 (표준 확률 문제)
choices = {
    1: Rational(1, 5),
    2: Rational(1, 4),
    3: Rational(1, 3),
    4: Rational(1, 2),
    5: Rational(2, 3)
}

# 주어진 조건
P_A = Rational(2, 3)
P_A_cap_B = Rational(2, 15)

# 핵심 관계식: P(A ∩ B) = P(A) × P(B) (A와 B 독립)
# 따라서 P(A ∩ B) = P(A) × P(B) 를 P(B)에 대해 풀기
P_B = symbols('P_B', positive=True, real=True)
equation = Eq(P_A_cap_B, P_A * P_B)
P_B_value = solve(equation, P_B)[0]

# CANDIDATE 선택지가 정답인지 검증
if choices[CANDIDATE] == P_B_value:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")