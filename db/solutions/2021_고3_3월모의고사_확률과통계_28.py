from itertools import product
X = [1,2,3,4,5]
Y = [2,4,6,8,10,12]
count = 0
for f1,f2,f3,f4,f5 in product(Y, repeat=5):
    if f2 < f3 < f4 and f1 > f3 > f5:
        count += 1
print('VERIFY_PASS' if count == 104 else 'VERIFY_FAIL')