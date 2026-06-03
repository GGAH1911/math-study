m_val, n_val = 2, 4
def f(x):
    return x * (x - m_val) * (x - n_val)
f1, f3, f5 = f(1), f(3), f(5)
cond1 = f1 * f3 < 0
cond2 = f3 * f5 < 0
f6 = f(6)
if cond1 and cond2 and f6 == 48:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'f(1)={f1}, f(3)={f3}, f(5)={f5}, f(1)f(3)={f1*f3}, f(3)f(5)={f3*f5}, f(6)={f6}')