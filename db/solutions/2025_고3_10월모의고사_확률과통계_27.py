from itertools import product

count = 0
for a in range(1, 145):
    if a % 2 == 0 and 144 % a == 0:
        remainder = 144 // a
        for b in range(1, remainder + 1):
            if remainder % b == 0:
                c = remainder // b
                if a * b * c == 144:
                    count += 1

if count == 60:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')