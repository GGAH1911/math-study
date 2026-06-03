# A: 6의 배수 (50 이하)
A = {x for x in range(1, 51) if x % 6 == 0}

# B: 4의 배수 (50 이하)
B = {x for x in range(1, 51) if x % 4 == 0}

# A \ B 구하기
A_diff_B = A - B

# X는 A \ B의 부분집합이어야 함
# 가능한 X의 개수 = 2^|A \ B|
num_elements = len(A_diff_B)
num_subsets = 2 ** num_elements

print(f'A = {sorted(A)}')
print(f'B = {sorted(B)}')
print(f'A ∖ B = {sorted(A_diff_B)}')
print(f'|A ∖ B| = {num_elements}')
print(f'X의 개수 = 2^{num_elements} = {num_subsets}')

if num_subsets == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')