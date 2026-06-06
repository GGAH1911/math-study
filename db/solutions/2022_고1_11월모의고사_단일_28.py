from itertools import combinations
U = {1, 2, 4, 8, 16, 32}
A = {2, 4, 16}
B = {1, 8, 2}  # B-A = {1,8}
A_union_B = A | B
B_minus_A = B - A
B_complement = U - B
A_union_B_complement = A | B_complement
sum_A_union_B_complement = sum(A_union_B_complement)
sum_B_minus_A = sum(B_minus_A)
check1 = len(A_union_B) == 5
check2 = sum_A_union_B_complement == 6 * sum_B_minus_A
check3 = 2 <= len(B_minus_A) <= 4
if check1 and check2 and check3 and sum(A) == 22:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')