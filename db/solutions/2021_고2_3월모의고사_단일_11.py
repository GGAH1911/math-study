# 100 이하의 자연수
U = set(range(1, 101))

# A: 홀수
A = {x for x in U if x % 2 == 1}

# B: 7의 배수
B = {x for x in U if x % 7 == 0}

# A ∪ B
A_union_B = A | B
n_result = len(A_union_B)

if n_result == 57:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {n_result}, expected 57')