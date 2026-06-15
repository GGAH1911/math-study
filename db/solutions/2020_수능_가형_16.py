from itertools import product

count = 0
MAX_VAL = 20  # a+b+c <= 9+4=13이면 충분, 여유있게 20
for d in range(5):  # d <= 4
    for a in range(MAX_VAL+1):
        for b in range(MAX_VAL+1):
            for c in range(MAX_VAL+1):
                if a+b+c-d == 9 and c >= d:
                    count += 1

print('count =', count)
if count == 275:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
