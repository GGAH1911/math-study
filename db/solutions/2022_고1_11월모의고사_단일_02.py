A = {1, 2, 3, 4, 5, 6}
B = {2, 4, 6, 8}
result = A - B
if result == {1, 3, 5} and len(result) == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')