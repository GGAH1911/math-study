import sympy as sp

a = 5  # 구한 답

x = sp.Symbol('x')

# 원래 함수: y = log2(x) + 1
# x축 방향으로 a 평행이동: y = log2(x - a) + 1
# y = x 대칭이동(x와 y 교환): x = log2(y - a) + 1
# => 2^(x-1) = y - a => y = 2^(x-1) + a

derived = sp.Pow(2, x - 1) + a          # 변환 후 유도된 함수
target  = sp.Pow(2, x - 1) + 5          # 문제에서 요구하는 함수

diff = sp.simplify(target - derived)

if diff == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
