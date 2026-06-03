import math

def verify_solution():
    # Define a_n = 4n^2 + 8n + 3
    def a_n(n):
        return 4*n*n + 8*n + 3
    
    # Check condition (나): sqrt(a_n + 1) must be natural number
    for n in range(1, 6):
        val = a_n(n) + 1
        sqrt_val = math.sqrt(val)
        if sqrt_val != int(sqrt_val):
            print('VERIFY_FAIL')
            return
        expected = 2*n + 2
        if int(sqrt_val) != expected:
            print('VERIFY_FAIL')
            return
    
    # Check condition (가): lim(sqrt(a_n) - 2n) = 2
    limit_sum = 0
    for n in range(1000, 1100):
        limit_sum += math.sqrt(a_n(n)) - 2*n
    limit_approx = limit_sum / 100
    if abs(limit_approx - 2.0) > 0.01:
        print('VERIFY_FAIL')
        return
    
    # Check answer: a_2/a_1 = 7/3
    ratio = a_n(2) / a_n(1)
    expected_ratio = 7/3
    if abs(ratio - expected_ratio) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')

verify_solution()