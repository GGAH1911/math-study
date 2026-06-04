# 원래 문제: f(1) × f(2) ≠ 4를 만족하는 함수의 개수
# Y = {1, 2, 3}에서 두 원소의 곱이 4가 되는 경우는 2×2=4만 가능

count_total = 0
count_f1f2_eq4 = 0

# 모든 함수 열거
for f1 in [1, 2, 3]:
    for f2 in [1, 2, 3]:
        for f3 in [1, 2, 3]:
            for f4 in [1, 2, 3]:
                for f5 in [1, 2, 3]:
                    count_total += 1
                    if f1 * f2 == 4:
                        count_f1f2_eq4 += 1

result = count_total - count_f1f2_eq4
if result == 216:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')