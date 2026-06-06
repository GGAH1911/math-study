import math

# x = 4에서 최댓값을 가지는지 검증
x = 4
AB = 2 * math.log2(x)
AC = math.log(16/x, 4)
S = 0.5 * AB * AC

print(f'x = {x}일 때:')
print(f'AB = {AB}')
print(f'AC = {AC}')
print(f'S(x) = {S}')
print(f'M = {S}')

# 근처 점들에서 확인
t_values = [1, 1.5, 2, 2.5, 3]
for t in t_values:
    x = 2**t
    if 1 < x < 16:
        AB = 2 * math.log2(x)
        AC = math.log(16/x, 4)
        area = 0.5 * AB * AC
        print(f't = {t}: S = {area:.6f}')

# 최종 답
a = 4
M = 2.0
result = a + M
print(f'\na + M = {result}')
if abs(result - 6) < 0.001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')