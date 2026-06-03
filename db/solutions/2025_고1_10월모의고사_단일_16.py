from itertools import combinations, permutations

count = 0
students_1 = ['A1', 'A2', 'A3']
students_2 = ['B1', 'B2']
students_3 = ['C']
all_students = students_1 + students_2 + students_3

for selected in combinations(all_students, 5):
    for perm in permutations(selected):
        valid = True
        for i in range(len(perm) - 1):
            if perm[i] in students_1 and perm[i+1] in students_1:
                valid = False
                break
        if valid:
            count += 1

if count == 252:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {count}')