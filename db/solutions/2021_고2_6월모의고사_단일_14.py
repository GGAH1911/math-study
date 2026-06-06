import math

def f(x):
    if 0 < x <= 1:
        return 0
    else:
        return math.log(x, 3)

t_values = [1/9, 9]
for t in t_values:
    result = f(t) + f(1/t)
    if abs(result - 2) < 1e-10:
        print(f't={t}: f(t) + f(1/t) = {result} ✓')
    else:
        print(f't={t}: f(t) + f(1/t) = {result} ✗')

sum_t = sum(t_values)
expected = 82/9
if abs(sum_t - expected) < 1e-10:
    print(f'Sum = {sum_t} = {82}/{9}')
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')