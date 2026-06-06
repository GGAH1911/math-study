import math

# 주어진 조건: 4*log_64(3/(4n+16))이 정수
def verify(n):
    arg = 3 / (4*n + 16)
    if arg <= 0:
        return False
    # log_64(x) = log(x) / log(64)
    log_val = math.log(arg) / math.log(64)
    result = 4 * log_val
    # 정수인지 확인 (부동소수점 오차 고려)
    return abs(result - round(result)) < 1e-9

candidates = [2, 44, 380]
for n in candidates:
    if not verify(n):
        print('VERIFY_FAIL')
        exit()

print('VERIFY_PASS')