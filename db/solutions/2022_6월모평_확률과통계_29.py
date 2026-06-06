from itertools import permutations

numbers = [2, 3, 4, 5, 6]
count = 0

for perm in permutations(numbers):
    valid = True
    circle = [1] + list(perm)
    
    for i in range(len(circle)):
        a = circle[i]
        b = circle[(i+1) % len(circle)]
        if a * b == 12:
            valid = False
            break
    
    if valid:
        count += 1

if count == 48:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')