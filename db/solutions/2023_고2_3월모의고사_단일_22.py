A = {-7, -5, 3}
B = {-7, -5, 9}
intersection = A & B
product = 1
for elem in intersection:
    product *= elem
print('VERIFY_PASS' if product == 35 else 'VERIFY_FAIL')