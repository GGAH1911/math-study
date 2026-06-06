from sympy import *

def verify(a1_val):
    results = []
    
    # Case 1: a1=4, a2=3
    if a1_val == 4:
        a1, a2 = 4, 3
        a3 = a1 // 2  # a1 even
        a4 = a3 + a2  # a2 odd
        a5 = a3 // 2  # a3 even
        a6 = a5 + a4  # a4 odd
        results.append((a1, a2, a3, a4, a5, a6))
    
    # Case 2: a1 = 24 - 2*a2 for a2 in {1,3,5,7,9,11}
    for a2 in [1, 3, 5, 7, 9, 11]:
        if a1_val == 24 - 2*a2:
            a1 = a1_val
            a3 = a1 // 2  # a1 even
            a4 = a3 + a2  # a2 odd
            a5 = a4 + a3  # a3 odd
            a6 = a4 // 2  # a4 even
            results.append((a1, a2, a3, a4, a5, a6))
    
    if not results:
        return 'VERIFY_FAIL'
    
    for a1, a2, a3, a4, a5, a6 in results:
        if a6 != 6:
            return 'VERIFY_FAIL'
        even_count = sum(1 for x in [a2, a3, a4, a5] if x % 2 == 0)
        if even_count != 1:
            return 'VERIFY_FAIL'
    
    return 'VERIFY_PASS'

# Test all possible a1 values
for a1 in [2, 4, 6, 10, 14, 18, 22]:
    if verify(a1) != 'VERIFY_PASS':
        print('VERIFY_FAIL')
        exit()

print('VERIFY_PASS')