A = {3, 6, 9}
B = {1, 2, 6, 9}
intersection = A & B
expected_sum = sum(intersection)
answer = 15
if expected_sum == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')