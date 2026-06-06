from math import factorial, comb, perm
total = factorial(7)
event_A = 2520
event_C = 960
event_AC = 480
result = (event_A + event_C - event_AC) / total
expected = 25 / 42
if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {result} != {expected}')