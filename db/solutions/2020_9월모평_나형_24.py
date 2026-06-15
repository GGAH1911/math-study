# 2020 9월모평 나형 24: a_{n+1}+a_n = 3n-1, a3=4. a1+a5?
CANDIDATE = 8
a3 = 4
a2 = (3 * 2 - 1) - a3    # n=2: a3+a2 = 5
a1 = (3 * 1 - 1) - a2    # n=1: a2+a1 = 2
a4 = (3 * 3 - 1) - a3    # n=3: a4+a3 = 8
a5 = (3 * 4 - 1) - a4    # n=4: a5+a4 = 11
print('VERIFY_PASS' if a1 + a5 == CANDIDATE else 'VERIFY_FAIL')
