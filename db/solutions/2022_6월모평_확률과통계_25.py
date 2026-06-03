from fractions import Fraction

# 전체 경우의 수
total = 5**4

# 3500보다 큰 네 자리 수 개수
count_greater = 0

# 첫 자리 1~5, 둘째 자리~네째 자리 1~5로 모든 경우 확인
for d1 in range(1, 6):
    for d2 in range(1, 6):
        for d3 in range(1, 6):
            for d4 in range(1, 6):
                number = d1 * 1000 + d2 * 100 + d3 * 10 + d4
                if number > 3500:
                    count_greater += 1

# 확률 계산
probability = Fraction(count_greater, total)
expected = Fraction(11, 25)

if probability == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')