from math import factorial

def perm(n, r):
    return factorial(n) // factorial(n - r)

def rep_perm(n, r):
    return n ** r

result = perm(3, 2) + rep_perm(3, 2)
# 정답 확인: 보기 ①=15
if result == 15:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}')
