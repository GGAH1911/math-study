from sympy import symbols, Eq

CANDIDATE = 5

# 선택지 (보기 ①~⑤)
choices = [10, 11, 12, 13, 14]
expected_answer = choices[CANDIDATE - 1]  # CANDIDATE=5 -> choices[4] = 14

# 수열 {a_n} 규칙에 따른 단계별 계산
a1 = 1  # 주어진 초기값

# 단계 1: a_1 = 1 (홀수) -> a_2 = 3*a_1 - 1
a2 = 3 * a1 - 1  # = 2

# 단계 2: a_2 = 2 (짝수) -> a_3 = (a_2)^2 + 1
a3 = a2**2 + 1  # = 5

# 단계 3: a_3 = 5 (홀수) -> a_4 = 3*a_3 - 1
# 핵심 관계식: a_4 = 3*a_3 - 1
a4_relation = Eq(symbols('a4'), 3*a3 - 1)
a4_value = a4_relation.rhs  # 14

# 검증: 계산된 a_4가 CANDIDATE(5번 선택지)와 일치하는가?
if a4_value == expected_answer:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")