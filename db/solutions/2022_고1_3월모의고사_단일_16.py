import numpy as np
from fractions import Fraction

# Case 1: a = -1/3, b = 7/6
a_case1 = Fraction(-1, 3)
b_case1 = Fraction(7, 6)

# 검증
fr1 = Fraction(1, 6)
fr2 = Fraction(2, 3)

# 수열 확인
seq1 = [a_case1, fr1, fr2, b_case1]
seq1_sorted = sorted(seq1)

# 공차 확인
diff1 = seq1_sorted[1] - seq1_sorted[0]
diff2 = seq1_sorted[2] - seq1_sorted[1]
diff3 = seq1_sorted[3] - seq1_sorted[2]

# 모두 같은지 확인
if diff1 == diff2 == diff3:
    # ab < 0 확인
    if a_case1 * b_case1 < 0:
        result_sum = a_case1 + b_case1
        if result_sum == Fraction(5, 6):
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')