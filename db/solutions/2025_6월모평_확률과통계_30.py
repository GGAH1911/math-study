from itertools import product
X = {-2, -1, 0, 1, 2}
count = 0
for f_minus2, f_minus1, f_0, f_1, f_2 in product([0,1,2], [-1,0,1,2], X, [-2,-1,0,1], [-2,-1,0]):
    # 조건 (가): x + f(x) ∈ X
    if not ((-2 + f_minus2 in X) and (-1 + f_minus1 in X) and (0 + f_0 in X) and (1 + f_1 in X) and (2 + f_2 in X)):
        continue
    # 조건 (나): f(-2) >= f(-1) >= f(0) >= f(1) >= f(2)
    if f_minus2 >= f_minus1 >= f_0 >= f_1 >= f_2:
        count += 1
if count == 108:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')