from sympy import divisors

# 14의 약수
divisors_14 = divisors(14)
print(f'14의 약수: {divisors_14}')

# 순서쌍 (a, b) 찾기
count = 0
valid_pairs = []
for a in range(1, 7):
    for b in range(1, 7):
        if (a + b) in divisors_14:
            count += 1
            valid_pairs.append((a, b))

print(f'조건을 만족하는 순서쌍: {valid_pairs}')
print(f'개수: {count}')

if count == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')