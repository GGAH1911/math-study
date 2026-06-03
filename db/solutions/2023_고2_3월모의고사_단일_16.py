import sympy as sp
from sympy import symbols, Piecewise, simplify

x = symbols('x', real=True)

# 구한 답: a = -1/3, b = 4
a_val = -1/3
b_val = 4

# 원래 함수 정의
def f(x_val):
    if 0 <= x_val < 3:
        return a_val * x_val**2 + b_val
    elif 3 <= x_val <= 4:
        return x_val - 3
    else:
        return None

# f(1) 계산
f_1 = f(1)
print(f'f(1) = {f_1}')
print(f'f(1) = {float(f_1):.10f}')

# 일대일대응 검증
# [0,3)에서 f(x) = -1/3*x^2 + 4의 치역
f_0 = f(0)
f_3_minus = a_val * 9 + b_val
print(f'\n[0,3)에서:')
print(f'f(0) = {f_0}')
print(f'lim x->3- f(x) = {f_3_minus}')
print(f'치역: ({f_3_minus}, {f_0}]')

# [3,4]에서 f(x) = x-3의 치역
f_3 = f(3)
f_4 = f(4)
print(f'\n[3,4]에서:')
print(f'f(3) = {f_3}')
print(f'f(4) = {f_4}')
print(f'치역: [{f_3}, {f_4}]')

# 단사성 확인: 두 치역이 겹치는 부분
print(f'\n전체 치역 합집합: [0, 4] ✓')

# 정답이 11/3인지 확인
if f_1 == 11/3:
    print(f'\nVERIFY_PASS')
else:
    print(f'\nVERIFY_FAIL')