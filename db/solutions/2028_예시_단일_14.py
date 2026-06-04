import sympy as sp

k = -2
a1 = 2 + 6*k
a2 = a1 - 2*k
a3 = a2 - 2*k
a4 = a3 - 2*k

if a4 != 2:
    print('VERIFY_FAIL')
else:
    a5 = k*a4 + 2
    a6 = k*a5 + 2
    a7 = k*a6 + 2
    
    if a1 == a7 and a4 == 2:
        result = abs(a1) + abs(a2)
        if result == 16:
            print('VERIFY_PASS')
        else:
            print('VERIFY_FAIL')
    else:
        print('VERIFY_FAIL')