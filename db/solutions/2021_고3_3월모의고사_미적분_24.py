import sympy as sp

x = sp.Symbol('x')

# 답: x가 -1, 0, 1, 2, 3, 4, 5일 때 수렴
test_values = [-1, 0, 1, 2, 3, 4, 5]
count = 0

for x_val in test_values:
    r = (x_val**2 - 4*x_val) / 5
    # 수렴 조건 검증: -1 < r <= 1
    if -1 < r <= 1:
        count += 1

# 경계 바깥의 값들도 확인
for x_val in [-2, 6]:
    r = (x_val**2 - 4*x_val) / 5
    if -1 < r <= 1:
        count += 1

if count == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')