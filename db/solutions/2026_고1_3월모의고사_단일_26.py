import numpy as np

data = np.array([-2, 1, 7, 6, -3, 3])

# 중앙값 검증
sorted_data = np.sort(data)
median = (sorted_data[2] + sorted_data[3]) / 2

if median == 2:
    # 분산 계산
    variance = np.var(data, ddof=0)
    answer = 14
    
    if abs(variance - answer) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')