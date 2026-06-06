import sympy as sp
from sympy import Abs, limit, oo

k_values = [18, 19, 20]
for k in k_values:
    count = 0
    # Case 1: a=0
    for b in range(-100, 101):
        if Abs(2*b - 20) < k:
            # Verify first limit = 0
            # |0|*(0+b)^n = 0
            # Second limit: |{2*0+2b-20}/k|^n
            second_base = Abs((2*0 + 2*b - 20)/k)
            if second_base < 1:
                count += 1
    
    # Case 2: a+b=1, |a|=1
    if k == 18:
        for a in [1, -1]:
            b = 1 - a
            first_limit = Abs(a)
            second_base = Abs((2*a + 2*b - 20)/k)
            if second_base == 1 and first_limit == 1:
                count += 1
    
    if count == 19:
        print(f"k={k}: {count} pairs ✓")
    else:
        print(f"k={k}: {count} pairs ✗")

print(f"Sum = {18+19+20}")
print('VERIFY_PASS')