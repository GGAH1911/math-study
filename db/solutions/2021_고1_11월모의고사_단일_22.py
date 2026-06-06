# 원래 문제의 조건으로 검증
A = {2, 5}
B = {2, 4, 5}  # a = 5를 대입

# A ⊂ B 확인: A의 모든 원소가 B에 포함되는가?
if A.issubset(B):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')