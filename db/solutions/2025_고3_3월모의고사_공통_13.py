import numpy as np

def f(x, a):
    return a * np.sin(x) if x < 0 else 1 - np.cos(x)

def check_a(a):
    xs = np.linspace(-np.pi, np.pi, 200001)
    vals = np.array([f(x, a) for x in xs])
    M, m = vals.max(), vals.min()
    return abs((M - m) - 4) < 1e-4

a_values = [2, -4]
all_pass = all(check_a(a) for a in a_values)
product = 1
for a in a_values:
    product *= a

if all_pass and product == -8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
