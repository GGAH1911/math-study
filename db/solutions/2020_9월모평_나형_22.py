from sympy import binomial

# 2020 9월모평 나형 22: 8C6 의 값.
CANDIDATE = 28
print('VERIFY_PASS' if binomial(8, 6) == CANDIDATE else 'VERIFY_FAIL')
