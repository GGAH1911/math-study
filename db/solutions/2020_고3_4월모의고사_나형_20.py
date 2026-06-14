from sympy import log, symbols, simplify, N
from sympy import Rational as R

# 문제 조건: 두 함수
# f(x) = 2^x, g(x) = 2^(x-2)
# 역함수: f_inv(y) = log_2(y), g_inv(y) = log_2(y) + 2

# 답: a = 6, b = 9
a = 6
b = 9

# 조건 검증
# (1) a < b 확인
assert a < b, 'a < b 실패'

# (2) a와 b가 양수 확인
assert a > 0 and b > 0, '양수 조건 실패'

# (3) 조건 (나): g^{-1}(b) - f^{-1}(a) = log_2(6)
# f^{-1}(a) = log_2(a) = log_2(6)
# g^{-1}(b) = log_2(b) + 2 = log_2(9) + 2
f_inv_a = log(a, 2)
g_inv_b = log(b, 2) + 2
diff = simplify(g_inv_b - f_inv_a)
target = log(6, 2)

# 차이 확인
error = simplify(diff - target)
assert abs(N(error)) < 1e-10, f'조건 (나) 실패: {N(diff)} != {N(target)}'

# (4) 조건 (가): 넓이 = 6
# y축 방향 적분: ∫[a,b] (x_g(y) - x_f(y)) dy
# = ∫[a,b] ((log_2(y) + 2) - log_2(y)) dy
# = ∫[a,b] 2 dy = 2(b - a)
area = 2 * (b - a)
assert abs(area - 6) < 1e-10, f'조건 (가) 실패: 넓이 = {area} != 6'

print('VERIFY_PASS')