from fractions import Fraction

# 경우 1: a1 = 2/3
a1_case1 = Fraction(2, 3)
a2_case1 = a1_case1 - 3
a3_case1 = -2 * a2_case1 if a2_case1 < 0 else a2_case1 - 3
condition1 = (a3_case1 == a1_case1 + 4)

# 경우 2: a1 = -7/3
a1_case2 = Fraction(-7, 3)
a2_case2 = -2 * a1_case2
a3_case2 = a2_case2 - 3
condition2 = (a3_case2 == a1_case2 + 4)

# 전체 합
total_sum = a1_case1 + a1_case2
expected_answer = Fraction(-5, 3)

if condition1 and condition2 and total_sum == expected_answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')