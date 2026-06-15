from sympy import binomial

# 2020 6월모평 나형 22: 9C7 의 값을 구하시오.
CANDIDATE = 36
value = binomial(9, 7)            # 문제 조건: 9C7 을 직접 계산
print('VERIFY_PASS' if value == CANDIDATE else 'VERIFY_FAIL')
