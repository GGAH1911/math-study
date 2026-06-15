from itertools import combinations

# U = {1, 2, ..., 19}
U = set(range(1, 20))

# 조건 (가): a in A => 2a not in A
def satisfies_condition_a(A):
    for a in A:
        if 2*a in A:
            return False
    return True

# 조건 (나): A의 원소 합이 짝수
def satisfies_condition_b(A):
    return sum(A) % 2 == 0

max_size = 0
max_sum_for_max_size = 0

# 모든 부분집합을 확인
for r in range(1, 20):
    for A in combinations(sorted(U), r):
        A_set = set(A)
        if satisfies_condition_a(A_set) and satisfies_condition_b(A_set):
            if len(A) > max_size:
                max_size = len(A)
                max_sum_for_max_size = sum(A)
            elif len(A) == max_size:
                max_sum_for_max_size = max(max_sum_for_max_size, sum(A))

if max_sum_for_max_size == 148:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: got {max_sum_for_max_size}")