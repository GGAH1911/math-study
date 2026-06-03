import sympy as sp

# 검증: d_b = 2인 경우
a1, b1 = 3, 11
da, db = 4, 2

# 수열 정의
def a(n): return a1 + (n-1)*da
def b(n): return b1 + (n-1)*db

# 조건 확인
cond1 = (a(5) == b(5))  # a_5 - b_5 = 0
cond2 = (a(6) == b(7))  # a_6 - b_7 = 0
cond3 = (a(7) == 27)     # a_7 = 27
cond4 = (b(7) <= 24)     # b_7 <= 24

# 자연수 조건 (처음 10항까지)
all_natural = all(a(n) >= 1 and b(n) >= 1 for n in range(1, 11))

if cond1 and cond2 and cond3 and cond4 and all_natural:
    result = b1 - a1
    if result == 8:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')