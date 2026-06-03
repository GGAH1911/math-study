from sympy import symbols, solve, simplify

# 등비수열의 조건
a1 = 3  # a₁ = 3
r = 2   # r² = 4에서 r = 2 (양수)

# 각 항 계산
a3 = a1 * r**2
a4 = a1 * r**3
a5 = a1 * r**4

# 조건 검증
condition1 = (a1 == 3)  # a₁ = 3
condition2 = (a5 / a3 == 4)  # a₅/a₃ = 4

# 모든 항이 양수인지 확인 (a1, a3, a4, a5 > 0)
all_positive = a1 > 0 and a3 > 0 and a4 > 0 and a5 > 0

if condition1 and condition2 and all_positive and a4 == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')