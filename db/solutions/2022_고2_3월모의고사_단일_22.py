# 주어진 조건 검증
A = {6, 8}
a = 8
B = {a, a+2}
A_union_B = A.union(B)
print('A:', A)
print('B:', B)
print('A ∪ B:', A_union_B)
expected_union = {6, 8, 10}
if A_union_B == expected_union:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')