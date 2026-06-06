import sympy as sp
x = sp.Symbol('x')
m, a = 1, 2

# 조건 확인
# f(1) = 0 확인
f_at_1 = 1 + (a-1)*1 - a**2 + 2
print(f'f(1) = {f_at_1}')  # 0이어야 함

# f(2-)와 f(2+) 계산
f_left_2 = 4 + 2*1 - 4 + 2
f_right_2 = -3*2 + 4*2
print(f'f(2-) = {f_left_2}, f(2+) = {f_right_2}')

# g(2-)와 g(2+) 계산
g_left_2 = 2*2 - 2
g_right_2 = 2 - 1
print(f'g(2-) = {g_left_2}, g(2+) = {g_right_2}')

# 극한 검사
lim_left = f_left_2 / g_left_2
lim_right = f_right_2 / g_right_2
print(f'lim(x->2-) f/g = {lim_left}')
print(f'lim(x->2+) f/g = {lim_right}')
print(f'극한 존재: {lim_left == lim_right}')

# g(a^2) 계산
a_squared = a**2
result = a_squared - a + 1 if a_squared > m + 1 else a*a_squared - a
print(f'g({a_squared}) = {a_squared} - {a} + 1 = {result}')

final = m + result
print(f'\nm + g(a^2) = {m} + {result} = {final}')

if lim_left == lim_right and f_at_1 == 0:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')