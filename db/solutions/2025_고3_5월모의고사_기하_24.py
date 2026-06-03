import numpy as np
from sympy import symbols, solve, Abs

a_vals = [1, 4]
for a_val in a_vals:
    a = float(a_val)
    # 타원: x^2/a^2 + y^2/4 = 1
    # a^2와 4 비교
    a_sq = a**2
    semi_major = max(a_sq, 4)
    semi_minor = min(a_sq, 4)
    
    major_length = 2 * np.sqrt(semi_major)
    minor_length = 2 * np.sqrt(semi_minor)
    
    # 조건: 장축의 길이 = 단축의 길이의 2배
    condition_check = np.isclose(major_length, 2 * minor_length)
    assert condition_check, f'a={a_val}: major={major_length}, minor={minor_length}'

total = sum(a_vals)
assert total == 5, f'Sum mismatch: {total}'
print('VERIFY_PASS')