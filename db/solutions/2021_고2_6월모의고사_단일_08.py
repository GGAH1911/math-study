a = 5/16
b = 5/4

def f(x):
    return a * (2 ** (2*x))

f_at_1 = f(1)
f_at_2 = f(2)

max_val = f_at_2
min_val = f_at_1

if abs(max_val - 5) < 1e-10 and abs(min_val - b) < 1e-10 and abs(a + b - 25/16) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')