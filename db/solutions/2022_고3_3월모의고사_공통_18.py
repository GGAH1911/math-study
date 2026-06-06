import math

# 좌변 계산
left = sum(2**(k-1) for k in range(1, 6))
print(f'Left: {left}')
assert left == 31

# 우변 계산
right = sum(2 * 3**(k-1) for k in range(1, 6))
print(f'Right: {right}')
assert right == 242

# 부등식을 만족하는 n 찾기
valid_n = []
for n in range(1, 100):
    middle = n**2  # sum of first n odd numbers
    if left < middle < right:
        valid_n.append(n)

print(f'Valid n: {valid_n}')
assert valid_n == list(range(6, 16))

# 합 계산
answer = sum(valid_n)
print(f'Sum: {answer}')
assert answer == 105

# 역대입 검증
for n in valid_n:
    middle = n**2
    assert 31 < middle < 242, f'n={n}: {31} < {middle} < {242} failed'

print('VERIFY_PASS')