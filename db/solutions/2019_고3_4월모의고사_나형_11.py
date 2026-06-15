from sympy import simplify

CANDIDATE = 1

answer_choices = {1: 5, 2: 6, 3: 7, 4: 8, 5: 9}

# 핵심 관계식: 8을 정확히 3개의 양의 정수로 분할
# 조건: a + b + c = 8, a ≥ b ≥ c ≥ 1 (빈 상자 없음, 순서 무관)

valid_solutions = []
for a in range(1, 8):
    for b in range(1, a + 1):
        c = 8 - a - b
        # 조건 확인: c는 양수이고, c ≤ b (내림차순)
        if c >= 1 and c <= b:
            # sympy로 합 조건 검증: a + b + c = 8
            check = simplify(a + b + c - 8)
            if check == 0:
                valid_solutions.append((a, b, c))

num_partitions = len(valid_solutions)
expected_value = answer_choices[CANDIDATE]

if num_partitions == expected_value:
    print("VERIFY_PASS")
else:
    print("VERIFY_FAIL")