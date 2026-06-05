import sympy as sp
x, a = sp.symbols('x a', real=True)
y = x**2 - 6*x + 10

# a = -2인 경우
a_val = -2
min_val_1 = min([float(y.subs(x, a_val)), float(y.subs(x, a_val+3))])
print(f'a={a_val}: min at x in [{a_val}, {a_val+3}] is {min_val_1}')

# a = 5인 경우
a_val = 5
min_val_2 = min([float(y.subs(x, a_val)), float(y.subs(x, a_val+3))])
print(f'a={a_val}: min at x in [{a_val}, {a_val+3}] is {min_val_2}')

# 최종 검증
if min_val_1 == 5 and min_val_2 == 5:
    total = -2 + 5
    if total == 3:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')