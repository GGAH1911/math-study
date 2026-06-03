# 원래 문제 조건: A ⊂ B
A = {1, 4}
B = {1, 2, 4}  # a = 4

# A ⊂ B 검증
if A.issubset(B):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')