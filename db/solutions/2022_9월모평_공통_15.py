import numpy as np
from fractions import Fraction

def f(a):
    if -1 <= a < -0.5:
        return -2*a - 2
    elif -0.5 <= a <= 0.5:
        return 2*a
    else:  # 0.5 < a <= 1
        return -2*a + 2

# 조건을 만족하는 모든 경로의 a1 값
a1_values = [Fraction(1), Fraction(1,2), Fraction(1,4), Fraction(3,4), 
             Fraction(1,8), Fraction(7,8), Fraction(3,8), Fraction(5,8)]

for a1 in a1_values:
    # Forward iteration
    a = float(a1)
    a2 = f(a)
    a3 = f(a2)
    a4 = f(a3)
    a5 = f(a4)
    a6 = f(a5)
    
    # Verify conditions
    assert abs(a5 + a6) < 1e-10, f"a5 + a6 != 0 for a1={a1}"
    assert a5 + a6 >= -1e-10, f"a5 + a6 < 0 for a1={a1}"
    
    sum_val = a + a2 + a3 + a4 + a5
    assert sum_val > -1e-10, f"sum < 0 for a1={a1}"

# Verify total sum
total = sum(a1_values)
assert total == Fraction(9, 2), f"Total sum is {total}, not 9/2"

print('VERIFY_PASS')