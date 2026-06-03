import numpy as np

def compute_Sn(n):
    # A_n, B_n: intersection of y=2nx and y=x^2+n^2-1
    xA, xB = n+1, n-1
    yA, yB = 2*n*xA, 2*n*xB
    # Verify on original curve
    assert abs(yA - (xA**2 + n**2 - 1)) < 1e-6, 'A_n not on curve'
    assert abs(yB - (xB**2 + n**2 - 1)) < 1e-6, 'B_n not on curve'
    # |A_n B_n|
    AB = np.sqrt((xA-xB)**2 + (yA-yB)**2)
    # Distance from circle center (2,0) to line 2nx - y = 0
    dist_center = abs(2*n*2 - 0) / np.sqrt((2*n)**2 + 1)
    # Max distance from circle (radius=1) to line
    max_dist = dist_center + 1
    return 0.5 * AB * max_dist

ratios = [compute_Sn(n)/n for n in [1000, 10000, 100000, 1000000]]
limit_approx = ratios[-1]
print(f'S_n/n ratios: {[round(r,6) for r in ratios]}')
print(f'Limit approx: {limit_approx:.8f}')
if abs(limit_approx - 6) < 1e-4:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {limit_approx}')
