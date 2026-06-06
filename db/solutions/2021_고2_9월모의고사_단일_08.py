from sympy import symbols, solve, log, simplify

# 답: m = 6, n = 2
m, n = 6, 2

# 평행이동된 함수: y = 3^(x-m) + n
# 조건 1: 점 (7, 5)를 지남
x, y = 7, 5
y_calc = 3**(x - m) + n
assert abs(y_calc - y) < 1e-9, f"점 (7, 5)를 지나지 않음: {y_calc}"

# 조건 2: 점근선이 y = 2 (지수함수의 점근선은 y = n)
assert n == 2, f"점근선이 y = {n}이 아님"

print('VERIFY_PASS')