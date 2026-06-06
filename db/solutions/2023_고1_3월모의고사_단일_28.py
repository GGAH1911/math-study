import math

# p=7, q=11
p, q = 7, 11

# 조건: p < q인 두 소수
assert p < q
assert all(p % i != 0 for i in range(2, int(math.sqrt(p))+1)) or p == 2  # p는 소수
assert all(q % i != 0 for i in range(2, int(math.sqrt(q))+1)) or q == 2  # q는 소수

# 범위 p^2*q < n <= p*q^2에 포함된 자연수 개수
lower_bound = p**2 * q
upper_bound = p * q**2
count = upper_bound - lower_bound

print(f'Lower bound: {lower_bound}')
print(f'Upper bound: {upper_bound}')
print(f'Count: {count}')
print(f'Expected: 308')

if count == 308:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')