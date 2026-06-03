import numpy as np

def f(x):
    if x < -2:
        return 1.0
    elif x <= -1:
        return 2*x + 2
    elif x <= 0:
        return -2*x - 2
    elif x < 1:
        return -x + 1
    else:
        return 2.0

eps = 1e-9
limit1 = f(-2 + eps)   # lim_{x→-2+}
limit2 = f(1 - eps)    # lim_{x→1-}
total = limit1 + limit2

print(f'lim_{{x->-2+}} f(x) = {limit1}')
print(f'lim_{{x->1-}} f(x) = {limit2}')
print(f'Sum = {total}')

if abs(total - (-2)) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
