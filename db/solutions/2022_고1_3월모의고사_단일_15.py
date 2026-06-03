students = [
    (30, 30), (30, 40), (30, 50),
    (40, 50),
    (50, 50), (50, 70), (50, 80),
    (60, 60), (60, 70), (60, 80), (60, 90),
    (70, 30), (70, 40), (70, 50),
    (80, 50), (80, 70), (80, 80),
    (90, 50), (90, 60), (90, 90),
]
n = len(students)
assert n == 20
same = sum(1 for x, y in students if x == y)
higher = sum(1 for x, y in students if y > x)
mean_x = sum(x for x, _ in students) / n
mean_y = sum(y for _, y in students) / n
g = (same == 5)
l = (higher == 8)
d = (mean_x > mean_y)
if g and l and d:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')