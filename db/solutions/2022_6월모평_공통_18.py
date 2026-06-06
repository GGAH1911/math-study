from sympy import sqrt, simplify

# 등비수열 정의
a = 36 * sqrt(3)
r = sqrt(3) / 3

# 주어진 조건 검증
a2 = a * r
a5 = a * r**4
a6 = a * r**5
a7 = a * r**6

# 조건 1: a2 = 36
cond1 = simplify(a2 - 36)

# 조건 2: a7 = (1/3) * a5
cond2 = simplify(a7 - a5/3)

if simplify(cond1) == 0 and simplify(cond2) == 0:
    # a6 값 확인
    result = simplify(a6)
    if result == 4:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')