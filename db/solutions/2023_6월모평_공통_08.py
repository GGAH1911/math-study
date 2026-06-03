import sympy as sp

# f(x) = 5x - 2가 최솟값 23을 달성하는 함수
def f(x):
    return 5*x - 2

def f_prime(x):
    return 5

# 조건 검증
# (가) f(1) = 3
assert f(1) == 3, f"f(1) = {f(1)}, expected 3"

# (나) 1 < x < 5에서 f'(x) >= 5
x_test = sp.Symbol('x')
for x_val in [1.5, 2, 3, 4, 4.5]:
    assert f_prime(x_val) >= 5, f"f'({x_val}) = {f_prime(x_val)} < 5"

# f(5)의 값
f_5 = f(5)
assert f_5 == 23, f"f(5) = {f_5}, expected 23"

# 이 함수가 조건을 만족하므로 f(5) >= 23이고, f(5) = 23 달성
print('VERIFY_PASS')