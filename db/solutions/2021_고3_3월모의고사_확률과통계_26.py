from itertools import combinations_with_replacement

# 연필 분배: 3명 학생에게 6자루를 나누되 각각 >=1개
count_pencil = 0
for x1 in range(1, 5):
    for x2 in range(1, 6-x1):
        x3 = 6 - x1 - x2
        if x3 >= 1:
            count_pencil += 1

# 지우개 분배: 3명 학생에게 5개를 나누되 각각 >=0개
count_eraser = 0
for z1 in range(0, 6):
    for z2 in range(0, 6-z1):
        z3 = 5 - z1 - z2
        if z3 >= 0:
            count_eraser += 1

total = count_pencil * count_eraser
print(f'Pencil distributions: {count_pencil}')
print(f'Eraser distributions: {count_eraser}')
print(f'Total: {total}')

if total == 210:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')