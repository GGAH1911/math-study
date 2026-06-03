from math import comb, factorial

# 원형 배열 수 = (n-1)!
circular = factorial(5 - 1)  # 4! = 24

# Case 1: 남학생 4명 + 여학생 1명
case1 = comb(5, 4) * comb(3, 1) * circular  # 5 * 3 * 24 = 360

# Case 2: 남학생 5명 + 여학생 0명
case2 = comb(5, 5) * comb(3, 0) * circular  # 1 * 1 * 24 = 24

total = case1 + case2

if total == 384:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {total}')
