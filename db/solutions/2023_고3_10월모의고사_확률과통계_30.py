from fractions import Fraction

# 초기 상태
# 흰공: 1, 2
# 검은공: 1, 2, 3

# 가능한 모든 경우와 그 결과를 추적
cases_with_sum_multiple_3 = []
cases_different_color = []

# 경우 3: 검은공 (1, 3) 선택
# 1을 다시 넣을 때: 최종 공 = {1(흰), 2(흰), 1(검), 2(검)}
final_sum_case3_1 = 1 + 2 + 1 + 2
if final_sum_case3_1 % 3 == 0:
    cases_with_sum_multiple_3.append(("검(1,3)-1넣기", 1/20, "같은색"))

# 경우 4: 검은공 (2, 3) 선택
# 2를 다시 넣을 때: 최종 공 = {1(흰), 2(흰), 1(검), 2(검)}
final_sum_case4_2 = 1 + 2 + 1 + 2
if final_sum_case4_2 % 3 == 0:
    cases_with_sum_multiple_3.append(("검(2,3)-2넣기", 1/20, "같은색"))

# 경우 6: 흰1, 검2 선택 (다른 색)
# 최종 공 = {2(흰), 1(검), 3(검)}
final_sum_case6 = 2 + 1 + 3
if final_sum_case6 % 3 == 0:
    cases_with_sum_multiple_3.append(("흰1,검2", 1/10, "다른색"))
    cases_different_color.append(("흰1,검2", 1/10))

# 경우 8: 흰2, 검1 선택 (다른 색)
# 최종 공 = {1(흰), 2(검), 3(검)}
final_sum_case8 = 1 + 2 + 3
if final_sum_case8 % 3 == 0:
    cases_with_sum_multiple_3.append(("흰2,검1", 1/10, "다른색"))
    cases_different_color.append(("흰2,검1", 1/10))

# 확률 계산
prob_sum_multiple_3 = sum(Fraction(p).limit_denominator() for _, p, _ in cases_with_sum_multiple_3)
prob_different_and_sum = sum(Fraction(p).limit_denominator() for _, p in cases_different_color)

conditional_prob = prob_different_and_sum / prob_sum_multiple_3

p = conditional_prob.denominator
q = conditional_prob.numerator

if p + q == 5 and conditional_prob == Fraction(2, 3):
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: {conditional_prob} p+q={p+q}")