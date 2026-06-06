A = {1, 3, 5, 7, 9}
B = {2, 5, 9}
intersection = A & B
print(f'A ∩ B = {sorted(intersection)}')
sum_elements = sum(intersection)
print(f'Sum of elements in A ∩ B: {sum_elements}')
if sum_elements == 14:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')