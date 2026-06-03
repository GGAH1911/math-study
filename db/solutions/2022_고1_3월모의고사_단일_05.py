# 히스토그램 데이터
intervals = {
    (3, 6): 5,
    (6, 9): 6,
    (9, 12): 9,
    (12, 15): 8,
    (15, 18): 7,
    (18, 21): 4
}

# 6시간 이상 12시간 미만인 학생 수
count = 0
for (start, end), students in intervals.items():
    if start >= 6 and end <= 12:
        count += students

print(count)
if count == 15:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')