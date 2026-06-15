from sympy import symbols, Eq, solve

# a_n = 2^(n+1) - 1로 표현
def a_n(n):
    return 2**(n+1) - 1

# 주어진 조건 확인
if a_n(4) == 31:
    a_2_value = a_n(2)
    # 점화식 검증
    valid = True
    for n in range(1, 4):
        if a_n(n+1) != 2*a_n(n) + 1:
            valid = False
            break
    if valid and a_2_value == 7:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')