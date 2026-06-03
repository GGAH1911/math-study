import math

# 원래 문제의 값들
log2_3 = math.log(3, 2)
log2_9 = math.log(9, 2)   # = 2*log2_3
log4_3 = math.log(3, 4)   # = log2_3 / 2
log9_8 = math.log(8, 9)   # = 3 / (2*log2_3)

t = log2_3

# 두 점 (0,0), (log2_9, k)를 지나는 직선의 기울기
# 수직 조건: m1 * m2 = -1
m1 = -log4_3 / log9_8   # 주어진 직선의 기울기

# m2 = k / log2_9
# m1 * m2 = -1 => k = -log2_9 / m1
k = -log2_9 / m1

result_3k = 3 ** k

print(f'log4_3 = {log4_3:.6f}')
print(f'log9_8 = {log9_8:.6f}')
print(f'log2_9 = {log2_9:.6f}')
print(f'm1 = {m1:.6f}')
print(f'k = {k:.6f}')
print(f'3^k = {result_3k:.6f}')

# 수직 조건 확인
m2 = k / log2_9
check = m1 * m2
print(f'm1*m2 = {check:.6f} (should be -1)')

if abs(result_3k - 64) < 1e-6 and abs(check + 1) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
