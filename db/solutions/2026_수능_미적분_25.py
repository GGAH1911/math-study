import numpy as np

def f(a_n, n):
    return (a_n + 2)**2 / (n * a_n + 5*n**2 - 2)

target = 5/2
passed = True

for n in [1000, 10000, 100000, 1000000]:
    lower_an = np.sqrt(9*n**2 - 5) + 2*n
    upper_an = 5*n + 1
    mid_an = (lower_an + upper_an) / 2  # 중간값 (항상 조건 만족)

    for a_n in [lower_an + 1e-9, mid_an, upper_an - 1e-9]:
        val = f(a_n, n)
        if abs(val - target) > 0.01:
            passed = False

if passed:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
