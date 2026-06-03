import numpy as np

def verify_answer():
    count = 0
    for a in range(1, 100):
        x_test = np.linspace(4.00001, 5.99999, 1000)
        condition = x_test**2 - 4*a*x_test + 3*a**2 > 0
        if not np.any(condition):
            count += 1
    print('VERIFY_PASS' if count == 3 else 'VERIFY_FAIL')

verify_answer()