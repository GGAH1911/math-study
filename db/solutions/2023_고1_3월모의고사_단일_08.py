# 도수분포표 조건 검증
total_students = 25
students_below_170 = 10  # 40% of 25

a = 2
students_160_170 = 8
b = 9
students_180_190 = 6

# 검증 1: 170cm 미만이 전체의 40%
below_170_actual = a + students_160_170
verify_1 = (below_170_actual == students_below_170)

# 검증 2: 전체 합이 25명
total_sum = a + students_160_170 + b + students_180_190
verify_2 = (total_sum == total_students)

# 검증 3: 170~180cm 학생이 구한 b값
verify_3 = (b == 9)

if verify_1 and verify_2 and verify_3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')