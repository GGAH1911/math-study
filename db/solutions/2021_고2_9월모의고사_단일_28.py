def verify_solution():
    def a_n(n):
        if n == 1:
            return 1
        elif n % 2 == 0:
            k = n // 2
            return (-1)**(k+1) * (2**k)
        else:
            k = (n - 1) // 2
            return (-1)**k * (2**k)
    
    # Check condition (가): S_{2n-1} = 1
    for n in range(1, 10):
        S = sum(a_n(i) for i in range(1, 2*n))
        if S != 1:
            print('VERIFY_FAIL')
            return False
    
    # Check condition (나): {a_n * a_{n+1}} is geometric with ratio -2
    products = [a_n(n) * a_n(n+1) for n in range(1, 18)]
    expected_ratio = -2
    for i in range(1, len(products)):
        if products[i] != products[i-1] * expected_ratio:
            print('VERIFY_FAIL')
            return False
    
    # Check S_10 = 33
    S10 = sum(a_n(i) for i in range(1, 11))
    if S10 != 33:
        print('VERIFY_FAIL')
        return False
    
    # Verify S_18 = 513
    S18 = sum(a_n(i) for i in range(1, 19))
    if S18 != 513:
        print('VERIFY_FAIL')
        return False
    
    print('VERIFY_PASS')
    return True

verify_solution()