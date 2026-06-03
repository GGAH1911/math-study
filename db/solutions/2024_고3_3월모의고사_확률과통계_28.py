from math import gcd

count = 0
for a in range(1, 721):
    for b in range(1, 27):  # b^2 <= 720 => b <= 26
        ab2 = a * b * b
        if ab2 > 720:
            break
        if 720 % ab2 == 0:
            c = 720 // ab2
            if gcd(a, c) > 1:
                count += 1

if count == 42:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')
