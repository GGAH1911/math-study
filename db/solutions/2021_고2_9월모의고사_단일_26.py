import sympy as sp
x = sp.Symbol('x')
f = 2*x**2 - 8*x + 9

# 검증 1: lim x->inf f(x)/(2x^2) = 1
lim1 = sp.limit(f / (2*x**2), x, sp.oo)
print(f'Condition 1: {lim1} == 1: {lim1 == 1}')

# 검증 2: lim x->1 (f(x)-3)/((x-1)(x-2)) = 4
lim2 = sp.limit((f - 3) / ((x-1)*(x-2)), x, 1)
print(f'Condition 2: {lim2} == 4: {lim2 == 4}')

# 답 계산
f_val = f.subs(x, 4)
print(f'f(4) = {f_val}')

if lim1 == 1 and lim2 == 4 and f_val == 9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')