from itertools import product

def check_condition(f):
    X = [1, 2, 3, 4]
    for a in X:
        for b in X:
            if f[a] >= b:
                if not (f[a] >= f[b]):
                    return False
    return True

X = [1, 2, 3, 4]
f1 = 3
min_sum = float('inf')

for f2, f3, f4 in product(X, repeat=3):
    f = {1: f1, 2: f2, 3: f3, 4: f4}
    if check_condition(f):
        current_sum = f2 + f4
        if current_sum < min_sum:
            min_sum = current_sum

if min_sum == 6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: min_sum = {min_sum}')