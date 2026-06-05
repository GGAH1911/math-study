import numpy as np

def f(x):
    return (1/3)**(x - 2) + 1

x_test = 0
f_at_0 = f(x_test)

x_vals = np.linspace(0, 4, 10000)
f_vals = np.array([f(x) for x in x_vals])
max_value = np.max(f_vals)

answer = 10

if np.isclose(f_at_0, answer) and np.isclose(max_value, answer):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')