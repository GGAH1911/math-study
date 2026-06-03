import numpy as np

def verify():
    # 조건을 만족하는 a_n 선택 (예: a_n = 2n + 3.5)
    # 극한값 계산
    results = []
    for n in [1000, 10000, 100000, 1000000]:
        a_n = 2*n + 3.5
        numerator = (a_n + 1)**2 + 6 * n**2
        denominator = n * a_n
        term = numerator / denominator
        results.append(term)
    
    # 극한값이 5에 수렴하는지 확인
    final_value = results[-1]
    if abs(final_value - 5.0) < 1e-4:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify()