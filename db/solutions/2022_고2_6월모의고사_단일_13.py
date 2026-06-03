import math

alpha = math.log2(3)
beta = math.log2(5)

# 원래 방정식에 대입하여 검증
x1 = alpha
result1 = 4**x1 - 2**(x1+3) + 15

x2 = beta
result2 = 4**x2 - 2**(x2+3) + 15

# 최종 답 계산
final_answer = 2**alpha * beta
expected = 3 * math.log2(5)

if abs(result1) < 1e-10 and abs(result2) < 1e-10 and abs(final_answer - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')