import math

k = 9
a = 1/3

def f(x):
    if x < k:
        return 0.5 * math.sin(math.pi * x)
    else:
        return (2/3)**(x - k) - 1

alpha = math.asin(2 * a) / math.pi
roots = []

# First piece: pairs in (2m+1, 2m+2) for m=0..3
for m in range(4):
    x1 = 2*m + 1 + alpha
    x2 = 2*m + 2 - alpha
    assert 0 <= x1 < k and 0 <= x2 < k
    assert abs(f(x1) + a) < 1e-10
    assert abs(f(x2) + a) < 1e-10
    roots.extend([x1, x2])

# Second piece
x_sec = k + math.log(1 - a) / math.log(2/3)
assert k <= x_sec <= 12
assert abs(f(x_sec) + a) < 1e-10
roots.append(x_sec)

total = sum(roots)
if abs(total - 46) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Sum={total}')
