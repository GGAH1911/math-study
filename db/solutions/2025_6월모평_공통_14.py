import math

def verify_condition(n, k):
    # 조건 1: -n^2 + 10n + 75 > 0
    expr1 = -n**2 + 10*n + 75
    if expr1 <= 0:
        return False
    
    # 조건 2: 75 - kn > 0
    expr2 = 75 - k*n
    if expr2 <= 0:
        return False
    
    # 조건 3: log_2 sqrt(-n^2+10n+75) - log_4(75-kn) > 0
    # 이는 -n^2+10n+75 > 75-kn과 동치
    if expr1 <= expr2:
        return False
    
    return True

# k=3과 k=6에서 조건 만족하는 n의 개수 확인
for k in [3, 6]:
    count = 0
    for n in range(1, 15):
        if verify_condition(n, k):
            count += 1
    if count == 12:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')