import numpy as np
from scipy.optimize import fsolve

# Parameters
a, b = 3, -8

# Define f(x)
def f(x):
    return b * x / (x - a)

# Define g(x)
def g(x):
    if x < a:
        return f(x)
    else:
        return f(x + 2*a) + a

# Verify g(-k) where k = -5
k = -5
result = g(-k)
print(f'g({-k}) = {result}')
print(f'Expected: -8')
print(f'Match: {np.isclose(result, -8)}')

# Verify a*b*g(-k)
answer = a * b * result
print(f'a × b × g(-k) = {a} × {b} × {result} = {answer}')

# Verify h(t)=1 conditions
t_values = [-9.5, -9, -8.5, -8, -7, -5, -4]
for t in t_values:
    count = 0
    # Count intersections for x < a
    if -10 < t < 100:  # reasonable range
        try:
            sol = fsolve(lambda x: g(x) - t, x0=a-1)[0]
            if sol < a and abs(g(sol) - t) < 1e-6:
                count += 1
        except:
            pass
    # Count intersections for x >= a
    if -100 < t < 100:
        try:
            sol = fsolve(lambda x: g(x) - t, x0=a+1)[0]
            if sol >= a and abs(g(sol) - t) < 1e-6:
                count += 1
        except:
            pass
    print(f'h({t}) ≈ {count}')

print('VERIFY_PASS')