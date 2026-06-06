A = {3, 8, 12}
B = {3, 5, 9}
difference = A - B
expected_sum = sum(difference)
print('VERIFY_PASS' if expected_sum == 20 else 'VERIFY_FAIL')