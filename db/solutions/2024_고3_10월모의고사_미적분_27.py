import math
import numpy as np

a = 3 * math.e
k = 1 / 3

def f(x):
    return math.exp(3 * x) - a * x

def g(x):
    return f(x) if x >= k else -f(x)

# Check 1: f(k) = 0 (continuity)
cont_check = abs(f(k)) < 1e-9

# Check 2: g is strictly increasing
xs = np.linspace(-10, 10, 5000)
g_vals = [g(float(x)) for x in xs]
monotone_check = all(g_vals[i] < g_vals[i+1] for i in range(len(g_vals)-1))

# Check 3: a * k == e
result = a * k
value_check = abs(result - math.e) < 1e-9

if cont_check and monotone_check and value_check:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: cont={cont_check}, monotone={monotone_check}, value={value_check}, a*k={result}')
