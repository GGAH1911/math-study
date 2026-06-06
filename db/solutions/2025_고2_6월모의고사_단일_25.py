import math

# 주기 조건으로부터 a 구하기
# 주기 = 2π/a = 4π
a = 2 * math.pi / (4 * math.pi)
print(f'a = {a}')

# f(x) = 6*cos(a*x) + 10
# f(4π/3) 계산
x = (4/3) * math.pi
result = 6 * math.cos(a * x) + 10

print(f'f(4π/3) = 6*cos({a}*{x:.4f}) + 10')
print(f'f(4π/3) = 6*cos(2π/3) + 10')
print(f'cos(2π/3) = {math.cos(2*math.pi/3):.4f}')
print(f'f(4π/3) = {result:.1f}')

# 검증
if abs(result - 7) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')