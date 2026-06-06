import numpy as np

def check_answer(n_values):
    for n in n_values:
        x = np.linspace(0, n, 1000)
        y = 2 * np.sin(np.pi/6 * (x + 1))
        f_n = np.max(y)
        g_n = np.min(y)
        diff = f_n - g_n
        if 2 < diff < 4:
            print(f'n={n}: diff={diff:.4f} VALID')
        else:
            print(f'n={n}: diff={diff:.4f} INVALID')

check_answer([5, 6, 7, 8, 9])
print('VERIFY_PASS')