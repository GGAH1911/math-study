import numpy as np

# 주어진 조건
A = np.array([1, 2])
P = np.array([2, 3])  # 내분점

# 풀이: 1:2로 내분하는 점 = (2*A + 1*B)/3 = P
# 따라서 B = (3*P - 2*A)/1 = 3*P - 2*A
B = 3 * P - 2 * A
a, b = B

print(f'a = {a}, b = {b}')
print(f'a + b = {a + b}')

# 검증: 1:2로 내분한 점이 (2, 3)인지 확인
P_calc = (2 * A + 1 * B) / 3
print(f'검증 내분점: {P_calc}')
print(f'주어진 내분점: {P}')

if np.allclose(P_calc, P):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')