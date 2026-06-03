import sympy as sp
x, a = sp.symbols('x a', real=True)

# a = 3 일 때 0 <= x <= 12 범위의 f(x) 정의
a_val = 3
def f_main(x_val):
    return a_val * (sp.sqrt(2*x_val + 1) + 1) / 2

# f(28) 계산: f(28) = f(4) + 6 + 6
f_4 = f_main(4)
f_16 = f_4 + 6
f_28 = f_16 + 6

print(f'f(4) = {f_4} = {float(f_4)}')
print(f'f(16) = f(4) + 6 = {f_16}')
print(f'f(28) = f(16) + 6 = {f_28}')

# 조건 검증: f(12) - f(0) = 6
f_0 = f_main(0)
f_12 = f_main(12)
diff = f_12 - f_0
print(f'\nVerification: f(12) - f(0) = {float(diff)}')

if abs(float(f_28) - 18) < 1e-9 and abs(float(diff) - 6) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')