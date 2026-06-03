# 주어진 조건을 만족하는 수열 구성
# a_n + b_n = n (모든 자연수 n)
# sum(3*a_k + 1, k=1..10) = 40

# 조건 2에서:
# sum(3*a_k + 1, k=1..10) = 40
# 3*sum(a_k) + 10 = 40
# sum(a_k) = 10

sum_a = 10  # from the given condition

# 조건 1에서:
# sum(a_k + b_k) = sum(k, k=1..10)
sum_k = sum(range(1, 11))  # 1+2+...+10 = 55

# sum(a_k) + sum(b_k) = sum(k)
sum_b = sum_k - sum_a
sum_b_computed = 55 - 10

print(f'sum_a = {sum_a}')
print(f'sum_k = {sum_k}')
print(f'sum_b = {sum_b_computed}')

# 검증: 조건을 만족하는 예시 수열 생성 (예: b_k = k, a_k = 0)
# 이는 a_1 + b_1 = 1을 만족하고, sum(3*a_k+1) = 10 = 40인지 확인 필요
# 더 정확한 검증: a_k들의 합이 10인지만 확인하면 됨

# 대안: 특정 a_k 값들을 찾음
# 예를 들어 a_1=1, a_2=1, ..., a_10=1이면 sum(a_k)=10
# 이 경우 b_k = k - a_k = k - 1
a_list = [1] * 10  # a_k = 1 for all k
sum_a_check = sum(a_list)
sum_3ak_plus_1 = sum(3*a + 1 for a in a_list)

print(f'\nVerification with a_k=1:')
print(f'sum(a_k) = {sum_a_check}')
print(f'sum(3*a_k+1) = {sum_3ak_plus_1}')

if sum_3ak_plus_1 == 40:
    b_list = [k - a for k, a in zip(range(1, 11), a_list)]
    sum_b_verify = sum(b_list)
    print(f'b_k values: {b_list}')
    print(f'sum(b_k) = {sum_b_verify}')
    if sum_b_verify == 45:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    # a_k=1이 아니므로 다른 분배 찾음
    # sum(a_k) = 10은 확정이므로 어떻게 분배하든 sum(b_k) = 45
    if sum_b_computed == 45:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')