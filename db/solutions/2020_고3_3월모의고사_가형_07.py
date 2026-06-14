from itertools import product
count = 0
for digits in product([0,1,2,3], repeat=4):
    if digits[0] == 0:
        continue  # not a four-digit natural number
    num = digits[0]*1000 + digits[1]*100 + digits[2]*10 + digits[3]
    if num < 2100:
        count += 1
print('VERIFY_PASS' if count == 80 else 'VERIFY_FAIL')