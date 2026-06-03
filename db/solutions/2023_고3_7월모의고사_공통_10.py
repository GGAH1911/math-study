import numpy as np

def verify():
    # 경우 1: sin(3x) = 0
    roots_case1 = []
    for k in range(6):
        x = k * np.pi / 3
        if 0 <= x < 2*np.pi:
            roots_case1.append(x)
    
    # 경우 2: sin(3x) = -1
    roots_case2 = []
    for k in range(3):
        x = (3*np.pi/2 + 2*k*np.pi) / 3
        if 0 <= x < 2*np.pi:
            roots_case2.append(x)
    
    all_roots = sorted(roots_case1 + roots_case2)
    
    # 각 근이 원래 방정식을 만족하는지 확인
    for x in all_roots:
        lhs = np.abs(4*np.sin(3*x) + 2)
        if not np.isclose(lhs, 2):
            print('VERIFY_FAIL')
            return
    
    if len(all_roots) == 9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()