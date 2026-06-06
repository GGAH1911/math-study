import numpy as np

total = 0
for n in range(1, 7):
    target = 1 / (2*n)
    alpha = np.arcsin(target)
    
    x1 = (2**n / np.pi) * alpha
    x2 = (2**n / np.pi) * (np.pi - alpha)
    
    val1 = 2 * np.sin(np.pi * x1 / (2**n))
    val2 = 2 * np.sin(np.pi * x2 / (2**n))
    
    assert abs(val1 - 1/n) < 1e-9, f'n={n}: val1 check failed'
    assert abs(val2 - 1/n) < 1e-9, f'n={n}: val2 check failed'
    assert abs((x1 + x2) - 2**n) < 1e-9, f'n={n}: sum check failed'
    
    total += 2**n

if abs(total - 126) < 0.01:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')