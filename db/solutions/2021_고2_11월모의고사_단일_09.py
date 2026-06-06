from math import log

# 원래 함수: f(x) = (1/2)^(x-a) + 1, a=3
a = 3

def f(x):
    return (0.5) ** (x - a) + 1

# 구간 [1, 3]에서 최댓값과 최솟값 확인
f_1 = f(1)
f_3 = f(3)

print(f'f(1) = {f_1}')
print(f'f(3) = {f_3}')

# 최댓값이 5인지 확인
max_val = max(f_1, f_3)
min_val = min(f_1, f_3)

print(f'최댓값: {max_val}')
print(f'최솟값: {min_val}')

if abs(max_val - 5) < 1e-9 and abs(min_val - 2) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')