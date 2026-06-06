# 원래 문제의 식으로 검증
x, y = 5, 1
eq1 = x - y - 4
eq2 = 2*x + y - 11
if eq1 == 0 and eq2 == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')