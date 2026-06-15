from itertools import product

count = 0
for x1 in range(13):
    for x2 in range(13):
        for x3 in range(13):
            for x4 in range(13):
                if (x2 - x1 >= 2 and 
                    x3 - x2 >= 2 and 
                    x4 - x3 >= 2 and 
                    x4 <= 12):
                    count += 1

if count == 210:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')